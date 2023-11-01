#ifndef RATES_BINDINGS_H
#define RATES_BINDINGS_H

#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace std;

void rates_bindings(py::module &m);

#endif //RATES_BINDINGS_H