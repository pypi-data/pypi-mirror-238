#ifndef CORE_BINDINGS_H
#define CORE_BINDINGS_H

#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace std;

void core_bindings(py::module &m);

#endif //CORE_BINDINGS_H