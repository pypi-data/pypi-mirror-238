#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <pybind11/pytypes.h>
#include "casters.h"
// #include <pybind11/chrono.h>
#include <datetime.h>
#include <chrono>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#include "date/date.h"
#include "date/date_bindings.h"
#include "rates/rates_bindings.h"
#include "core/core_bindings.h"


namespace py = pybind11;
using namespace std;
using namespace date;


PYBIND11_MODULE(python_quant_lib, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_quant_lib

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    py::object datetime_module = py::module::import("datetime");  // Use py::object for the datetime module
    py::object date_class = datetime_module.attr("date");

    date_bindings(m);
    rates_bindings(m);
    core_bindings(m);

#ifdef VERSION_INFO
    m.attr("__version__") = "dev";
    // m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
