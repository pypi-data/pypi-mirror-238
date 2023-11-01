#include <pybind11/pybind11.h>
#include <pybind11/chrono.h>

#include <string>
#include "context.h"
#include "../casters.h"
#include "configs.h"

namespace py = pybind11;
using namespace std;

void core_bindings(py::module &m)
{
    // Module Creation
    auto core_m = m.def_submodule("core", "Core related functionalities");

    py::class_<EvaluationContext>(core_m, "EvaluationContext")
        .def(py::init<const date::year_month_day &, const CalibrationConfig &>())
        .def("get_calendar", &EvaluationContext::get_calendar)
        .def("get_calendars", &EvaluationContext::get_calendars)
        .def("get_calibration_config", &EvaluationContext::get_calibration_config)
        .def("set_calendars", &EvaluationContext::set_calendars)
        .def_readonly("market_date", &EvaluationContext::market_date);

    py::class_<CalibrationConfig>(core_m, "CalibrationConfig")
        .def(py::init<const int &, const double &>());
};