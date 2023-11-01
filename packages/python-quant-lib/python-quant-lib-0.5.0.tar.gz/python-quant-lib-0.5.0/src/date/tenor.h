#ifndef TENOR_H
#define TENOR_H

#include "date.h"
#include "calendar.h"
#include <string>

using namespace std;

struct Tenor
{
    std::string value;
    int days = 0;
    int weeks = 0;
    int months = 0;
    int years = 0;
    Tenor(const std::string &tenor);

    Tenor operator+(const Tenor &other) const;
    Tenor operator-(const Tenor &other) const;
    Tenor operator*(int scalar) const;
    bool operator<(const Tenor &other) const;
};

// Tenors
date::year_month_day add_tenor(const date::year_month_day &date, const Tenor &tenor, const Calendar::HolidayCalendar &cal, const Calendar::BusinessDayConvention &bdc);

#endif // TENOR_H