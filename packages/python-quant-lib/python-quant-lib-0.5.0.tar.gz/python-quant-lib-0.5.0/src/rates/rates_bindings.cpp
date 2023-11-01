#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>

#include <string>
#include <variant>
#include "yield_curve.h"
#include "../casters.h"
#include "instruments.h"

namespace py = pybind11;
using namespace std;
using namespace YieldCurveModels;
using namespace YieldCurves;
using namespace LinearInstruments;

void rates_bindings(py::module &m)
{
    // Module Creation
    auto rates_m = m.def_submodule("rates", "Rates related functionalities");
    // Bindings
    py::class_<YieldCurve, std::unique_ptr<YieldCurve>>(rates_m, "YieldCurve")
        .def("_get_spot_rate", &YieldCurve::get_spot_rate)
        .def("_get_df", &YieldCurve::get_df)
        .def("_get_fwd", &YieldCurve::get_fwd)
        .def("_set_quotes", &YieldCurve::set_quotes);

    py::class_<NielsonSiegelSvenssonModel>(rates_m, "NielsonSiegelSvenssonModel")
        .def(py::init<double, double, double, double, double, double>())
        .def_readwrite("beta0", &NielsonSiegelSvenssonModel::beta0)
        .def_readwrite("beta1", &NielsonSiegelSvenssonModel::beta1)
        .def_readwrite("beta2", &NielsonSiegelSvenssonModel::beta2)
        .def_readwrite("beta3", &NielsonSiegelSvenssonModel::beta3)
        .def_readwrite("tau1", &NielsonSiegelSvenssonModel::tau1)
        .def_readwrite("tau2", &NielsonSiegelSvenssonModel::tau2)
        .def("_spot_rate", &NielsonSiegelSvenssonModel::spot_rate)
        .def("_df", &NielsonSiegelSvenssonModel::df);

    py::enum_<QuoteType>(rates_m, "QuoteType")
        .value("RATE", QuoteType::RATE)
        .value("SPREAD", QuoteType::SPREAD)
        .value("PRICE", QuoteType::PRICE)
        .value("CLEAN_PRICE", QuoteType::CLEAN_PRICE)
        .value("DIRTY_PRICE", QuoteType::DIRTY_PRICE);

    py::enum_<YieldCalcType>(rates_m, "YieldCalcType")
        .value("CURRENT_YIELD", YieldCalcType::CURRENT_YIELD)
        .value("SIMPLE_YIELD", YieldCalcType::SIMPLE_YIELD)
        .value("STREET", YieldCalcType::STREET);

    py::enum_<DiscountingType>(rates_m, "DiscountingType")
        .value("CONTINUOUS", DiscountingType::CONTINUOUS)
        .value("SIMPLE", DiscountingType::SIMPLE);

    py::class_<NSSBondCurve, YieldCurve>(rates_m, "NSSBondCurve")
        .def(py::init<std::string, date::year_month_day, NielsonSiegelSvenssonModel, Calendar::DayCountMethod, std::vector<LinearInstruments::DebtInstrument *> &, DiscountingType>());

    py::class_<DebtInstrument, std::unique_ptr<DebtInstrument>>(rates_m, "DebtInstrument")
        .def("_get_issuer", &DebtInstrument::get_issuer)
        .def("_get_currency", &DebtInstrument::get_currency)
        .def("_get_issue_date", &DebtInstrument::get_issue_date)
        .def("_get_maturity_date", &DebtInstrument::get_maturity_date)
        .def("_get_bdc", &DebtInstrument::get_bdc)
        .def("_get_dcm", &DebtInstrument::get_dcm)
        .def("_get_calendar", &DebtInstrument::get_calendar)
        .def("_get_quote", &DebtInstrument::get_quote)
        .def("_get_quote_type", &DebtInstrument::get_quote_type)
        .def("_get_settlement_lag", &DebtInstrument::get_settlement_lag)
        .def("_schedule", &DebtInstrument::schedule)
        .def("_flows", &DebtInstrument::flows)
        .def("_get_settlement_date", &DebtInstrument::get_settlement_date)
        .def("_set_quote", &DebtInstrument::set_quote);

    py::class_<Bill, DebtInstrument>(rates_m, "Bill")
        .def(py::init<const std::string &, const std::string &, const date::year_month_day &,
                      const date::year_month_day &, const Calendar::BusinessDayConvention &,
                      const Calendar::DayCountMethod &, const std::string &, const double &,
                      const QuoteType &, const double &, const Tenor &>())
        .def("_price", &Bill::price)
        .def("_discount_rate", &Bill::discount_rate);

    py::class_<Bond, DebtInstrument>(rates_m, "Bond")
        .def(py::init<const std::string &, const std::string &, const date::year_month_day &,
                      const date::year_month_day &, const date::year_month_day &,
                      const Calendar::BusinessDayConvention &, const Calendar::DayCountMethod &,
                      const std::string &, const double &, const double &, const QuoteType &, const double &,
                      const Tenor &, const Tenor &, const YieldCalcType &>())
        .def("_get_dated_date", &Bond::get_dated_date)
        .def("_get_coupon_rate", &Bond::get_coupon_rate)
        .def("_get_pay_freq", &Bond::get_pay_freq)
        .def("_accrued_interests", &Bond::accrued_interests)
        .def("_dirty_price", &Bond::dirty_price)
        .def("_clean_price", &Bond::clean_price)
        .def("_yield", &Bond::yield);
}