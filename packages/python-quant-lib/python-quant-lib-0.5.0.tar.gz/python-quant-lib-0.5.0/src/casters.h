#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <pybind11/pytypes.h>
#include <datetime.h>
#include "date/date.h"

using namespace date;

PYBIND11_NAMESPACE_BEGIN(PYBIND11_NAMESPACE)
PYBIND11_NAMESPACE_BEGIN(detail)

template <>
class type_caster<date::year_month_day> {
public:
    using type = date::year_month_day;
    bool load(handle src, bool) {
        // Lazy initialise the PyDateTime import
        if (!PyDateTimeAPI) {
            PyDateTime_IMPORT;
        }

        if (!src) {
            return false;
        }

        if (!PyDate_Check(src.ptr()))  // Check if the object is a datetime.date
            return false;

        PyObject* pydate = src.ptr();
        PyObject* year_obj = PyObject_GetAttrString(pydate, "year");
        PyObject* month_obj = PyObject_GetAttrString(pydate, "month");
        PyObject* day_obj = PyObject_GetAttrString(pydate, "day");

        int year = PyLong_AsLong(year_obj);
        unsigned int month = PyLong_AsLong(month_obj);
        unsigned int day = PyLong_AsLong(day_obj);

        Py_DECREF(year_obj);
        Py_DECREF(month_obj);
        Py_DECREF(day_obj);

        date::year_month_day ymd(date::year{year}, date::month{month}, date::day{day});
        value = ymd;

        return true;
    };

    static handle cast(const date::year_month_day &ymd,
                       return_value_policy /* policy */,
                       handle /* parent */) {
        // Lazy initialise the PyDateTime import
        if (!PyDateTimeAPI) {
            PyDateTime_IMPORT;
        }
        return PyDate_FromDate(int{ymd.year()}, (int)unsigned{ymd.month()}, (int)unsigned{ymd.day()});
    };

    PYBIND11_TYPE_CASTER(type, const_name("datetime.date"));
};

PYBIND11_NAMESPACE_END(detail)
PYBIND11_NAMESPACE_END(PYBIND11_NAMESPACE)