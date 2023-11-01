#include "yield_curve.h"
#include <cmath>
#include "../core/enums.h"
#include "../date/calendar.h"
#include "../core/context.h"
#include <Eigen/Dense>
#include <unsupported/Eigen/NonLinearOptimization>
#include <unsupported/Eigen/NumericalDiff>

using namespace std;
using namespace Eigen;

double YieldCurveModels::NielsonSiegelSvenssonModel::spot_rate(const double &t)
{
    double theta1 = t / this->tau1;
    double theta2 = t / this->tau2;
    double exp_term_1 = std::exp(-theta1);
    double exp_term_2 = std::exp(-theta2);
    double term1 = (1 - exp_term_1) / theta1;
    double term2 = term1 - exp_term_1;
    double term3 = (1 - exp_term_2) / theta2 - exp_term_2;
    return this->beta0 + this->beta1 * term1 + this->beta2 * term2 + this->beta3 * term3;
}

double YieldCurveModels::NielsonSiegelSvenssonModel::df(const double &t, const DiscountingType &discounting_type)
{
    switch (discounting_type)
    {
    case DiscountingType::CONTINUOUS:
        return std::exp(-this->spot_rate(t) * t);
    case DiscountingType::SIMPLE:
        return std::pow(1 / (1 + this->spot_rate(t)), t);
    }
    throw("Discounting Type: " + Enums::enumToString(discounting_type) + " is not supported");
}

double YieldCurves::NSSBondCurve::get_spot_rate(const EvaluationContext &ctx, const date::year_month_day &dt)
{
    this->calibrate(ctx);
    if (dt < this->curve_date)
    {
        throw("Cannot compute spot rate for a date in the past");
    }
    double t = year_frac(this->curve_date, dt, this->day_count);
    return this->model.spot_rate(t);
}

double YieldCurves::NSSBondCurve::get_df(const EvaluationContext &ctx, const date::year_month_day &dt)
{
    this->calibrate(ctx);
    if (dt < this->curve_date)
    {
        throw("Cannot compute spot rate for a date in the past");
    }
    double t = year_frac(this->curve_date, dt, this->day_count);
    return this->model.df(t, this->discounting_type);
}

double YieldCurves::NSSBondCurve::get_fwd(const EvaluationContext &ctx, const date::year_month_day &start, const date::year_month_day &end)
{
    return 0.0;
}

void YieldCurves::NSSBondCurve::set_quotes(const std::vector<std::tuple<double, QuoteType>> &quotes)
{
    this->_is_calibrated = false;
    this->model = YieldCurveModels::NielsonSiegelSvenssonModel(0.0, 0.0, 0.0, 0.0, 1.0, 1.0);
    for (int i = 0; i < quotes.size(); i++)
    {
        double quote = std::get<0>(quotes[i]);
        QuoteType quote_type = std::get<1>(quotes[i]);
        this->instruments[i]->set_quote(quote, quote_type);
    }
}

void YieldCurves::NSSBondCurve::calibrate(const EvaluationContext &ctx)
{
    if (this->_is_calibrated == false)
    {
        // we copy the context and ensure it uses the same date as the curve
        EvaluationContext new_ctx(ctx);
        new_ctx.market_date = this->curve_date;

        VectorXd x(6);
        x << model.beta0, model.beta1, model.beta2, model.beta3, model.tau1, model.tau2;
        int n_inputs = x.size();
        int m_values = (instruments.size());
        std::vector<double> prices;
        std::vector<PayFlows> flows;
        for (auto &inst : instruments)
        {
            if (LinearInstruments::Bill *bill_ptr = dynamic_cast<LinearInstruments::Bill *>(inst))
            {
                prices.push_back(bill_ptr->price(new_ctx));
            }
            else if (LinearInstruments::Bond *bond_ptr = dynamic_cast<LinearInstruments::Bond *>(inst))
            {
                prices.push_back(bond_ptr->dirty_price(new_ctx));
            }
            else
            {
                throw("Unsupported instrument type");
            }
            flows.push_back(inst->flows(new_ctx));
        }
        // Create the optimization problem
        Calibration::NSSCostFunction functor(n_inputs, m_values, prices, flows, curve_date, new_ctx, this->discounting_type);
        NumericalDiff<Calibration::NSSCostFunction> num_diff(functor);
        LevenbergMarquardt<NumericalDiff<Calibration::NSSCostFunction>> lm(num_diff);
        lm.parameters.maxfev = ctx.get_calibration_config().max_iter; // Maximum number of iterations
        // Call the optimizer
        auto info = lm.minimize(x);

        // Update the model parameters with the calibrated values
        model.beta0 = x[0];
        model.beta1 = x[1];
        model.beta2 = x[2];
        model.beta3 = x[3];
        model.tau1 = x[4];
        model.tau2 = x[5];

        if (info != 1)
        {
            // Calibration failed
            throw std::runtime_error("Calibration failed!");
        }
        this->_is_calibrated = true;
    }
}