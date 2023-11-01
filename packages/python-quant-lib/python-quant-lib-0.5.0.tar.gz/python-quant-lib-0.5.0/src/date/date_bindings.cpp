#include <pybind11/pybind11.h>

#include "tenor.h"
#include "calendar.h"
#include <string>
#include "date.h"
#include "../casters.h"

namespace py = pybind11;
using namespace std;

void date_bindings(py::module &m){
    //Module Creation
    auto date_m =  m.def_submodule("date", "Date Operations");
    //Bindings
    py::class_<Tenor>(date_m, "Tenor")
        .def(py::init<string>());
    py::class_<Calendar::HolidayCalendar>(date_m, "HolidayCalendar")
        .def(py::init<>());

    py::enum_<Calendar::BusinessDayConvention>(date_m, "BDC")
        .value("NO_ADJ", Calendar::BusinessDayConvention::NO_ADJ)
        .value("FOLLOWING", Calendar::BusinessDayConvention::FOLLOWING)
        .value("MODIFIED_FOLLOWING", Calendar::BusinessDayConvention::MODIFIED_FOLLOWING)
        .value("PRECEEDING", Calendar::BusinessDayConvention::PRECEEDING);

     py::enum_<Calendar::DayCountMethod>(date_m, "DCM")
        .value("ACT_ACT", Calendar::DayCountMethod::ACT_ACT)
        .value("ACT_360", Calendar::DayCountMethod::ACT_360)
        .value("ACT_365", Calendar::DayCountMethod::ACT_365)
        .value("ACT_365F", Calendar::DayCountMethod::ACT_365F);
    
    date_m.def("add_tenor", &add_tenor, R"pbdoc(
        Add a Tenor to a sepcific date
    )pbdoc");
    date_m.def("year_frac", &Calendar::year_frac, R"pbdoc(
        Compute the year frac between two dates
    )pbdoc");
};