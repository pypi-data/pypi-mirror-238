#ifndef DATE_BINDINGS_H
#define DATE_BINDINGS_H

#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace std;

void date_bindings(py::module &m);

#endif //DATE_BINDINGS_H