#ifndef YIELD_CURVE_H
#define YIELD_CURVE_H

#include <cmath>
#include <string>
#include <vector>
#include <map>
#include "../date/date.h"
#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <unsupported/Eigen/NonLinearOptimization>
#include <iostream>
#include "instruments.h"
#include "../date/calendar.h"
#include "../core/context.h"

using namespace std;
using namespace Eigen;

enum struct DiscountingType
{
    SIMPLE,
    CONTINUOUS
};

namespace YieldCurveModels
{

    struct NielsonSiegelSvenssonModel
    {
        double beta0 = 0.0; // level
        double beta1 = 0.0; // slope
        double beta2 = 0.0; // curvature
        double beta3 = 0.0; // long term rate
        double tau1 = 1.0;  // decay factor
        double tau2 = 1.0;  // persistence factor

        NielsonSiegelSvenssonModel();
        NielsonSiegelSvenssonModel(const double &beta0_, const double &beta1_, const double &beta2_, const double &beta3_, const double &tau1_, const double &tau2_) : beta0{beta0_}, beta1{beta1_}, beta2{beta2_}, beta3{beta3_}, tau1{tau1_}, tau2{tau2_} {};

        double spot_rate(const double &t);
        double df(const double &t, const DiscountingType &discounting_type);
    };
};

namespace YieldCurves
{
    class YieldCurve
    {
    public:
        virtual double get_spot_rate(const EvaluationContext &ctx, const date::year_month_day &dt) = 0;
        virtual double get_df(const EvaluationContext &ctx, const date::year_month_day &dt) = 0;
        virtual double get_fwd(const EvaluationContext &ctx, const date::year_month_day &start, const date::year_month_day &end) = 0;
        virtual void set_quotes(const std::vector<std::tuple<double, QuoteType>> &quotes) = 0;
    };

    class NSSBondCurve : public YieldCurve
    {
        std::string name;
        date::year_month_day curve_date;
        YieldCurveModels::NielsonSiegelSvenssonModel model;
        Calendar::DayCountMethod day_count;
        DiscountingType discounting_type;
        // TODO: Improve to support variants
        std::vector<LinearInstruments::DebtInstrument *> instruments;
        bool _is_calibrated = false;

        void calibrate(const EvaluationContext &ctx);

    public:
        NSSBondCurve(const std::string &name, const date::year_month_day &curve_date, const YieldCurveModels::NielsonSiegelSvenssonModel &model, const Calendar::DayCountMethod day_count, const std::vector<LinearInstruments::DebtInstrument *> &instruments, const DiscountingType &discounting_type) : name{name}, curve_date{curve_date}, model{model}, day_count{day_count}, instruments{instruments}, discounting_type{discounting_type} {};

        double get_spot_rate(const EvaluationContext &ctx, const date::year_month_day &dt) override;
        double get_df(const EvaluationContext &ctx, const date::year_month_day &dt) override;
        double get_fwd(const EvaluationContext &ctx, const date::year_month_day &start, const date::year_month_day &end) override;
        void set_quotes(const std::vector<std::tuple<double, QuoteType>> &quotes);
    };

};

namespace Calibration
{
    struct CalibrationConfig
    {
        int max_iter = 1e4;
        double x_tol = 1e-6;

        CalibrationConfig(){};
        CalibrationConfig(int max_iter_, double x_tol_) : max_iter{max_iter_}, x_tol{x_tol} {};
    };

    // Generic functor
    template <typename _Scalar, int NX = Eigen::Dynamic, int NY = Eigen::Dynamic>
    struct CalibrationFunctor
    {
        typedef _Scalar Scalar;
        enum
        {
            InputsAtCompileTime = NX,
            ValuesAtCompileTime = NY
        };
        typedef Eigen::Matrix<Scalar, InputsAtCompileTime, 1> InputType;
        typedef Eigen::Matrix<Scalar, ValuesAtCompileTime, 1> ValueType;
        typedef Eigen::Matrix<Scalar, ValuesAtCompileTime, InputsAtCompileTime> JacobianType;

        int m_inputs, m_values;

        CalibrationFunctor() : m_inputs(InputsAtCompileTime), m_values(ValuesAtCompileTime) {}
        CalibrationFunctor(int inputs, int values) : m_inputs(inputs), m_values(values) {}

        int inputs() const { return m_inputs; }
        int values() const { return m_values; }
    };

    struct NSSCostFunction : CalibrationFunctor<double>
    {

        std::vector<double> prices;
        std::vector<PayFlows> flows;
        date::year_month_day curve_date;
        const EvaluationContext &ctx;
        DiscountingType discounting_type;

        NSSCostFunction(
            const int m_inputs, const int m_values,
            std::vector<double> prices,
            std::vector<PayFlows> flows,
            const date::year_month_day &curve_date,
            const EvaluationContext &ctx,
            const DiscountingType &discounting_type) : CalibrationFunctor(m_inputs, m_values), prices{prices}, flows{flows}, curve_date{curve_date}, ctx{ctx}, discounting_type{discounting_type} {};

        int operator()(const VectorXd &x, VectorXd &fvec) const
        {
            // Calculate the model's spot rates and use them to calculate the error
            YieldCurveModels::NielsonSiegelSvenssonModel model(x[0], x[1], x[2], x[3], x[4], x[5]);
            for (size_t i = 0; i < prices.size(); ++i)
            {
                double value = 0.0;
                for (const auto &flow : flows[i])
                {
                    double yf = std::get<1>(flow);
                    double flow_val = std::get<2>(flow);
                    value += flow_val * model.df(yf, this->discounting_type);
                }
                fvec[i] = std::pow(prices[i] - value, 2);
            }
            return 0;
        }
    };

}

#endif // YIELD_CURVE_H