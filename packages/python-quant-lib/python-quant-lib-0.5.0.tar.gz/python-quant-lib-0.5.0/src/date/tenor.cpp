#include "tenor.h"
#include <regex>
#include <string>

#include <iostream>

using namespace std;

Tenor::Tenor::Tenor(const std::string &tenor)
{
    this->value = tenor;
    std::regex pattern("^(-?\\d+)(Y|M|W|D)$", std::regex_constants::icase);
    std::smatch match;
    if (std::regex_match(tenor, match, pattern))
    {
        int value = std::stoi(match.str(1));
        const std::string &type = match.str(2);
        if (type == "D" || type == "d")
        {
            this->days = value;
        }
        else if (type == "W" || type == "w")
        {
            this->weeks = value;
        }
        else if (type == "M" || type == "m")
        {
            this->months = value;
        }
        else
        {
            this->years = value;
        }
    }
    else
    {
        throw std::invalid_argument(tenor + " can't be parsed into a valid tenor");
    }
};

date::year_month_day add_tenor(const date::year_month_day &date, const Tenor &tenor, const Calendar::HolidayCalendar &cal, const Calendar::BusinessDayConvention &bdc)
{
    date::year_month_day new_date = date + date::years(tenor.years) + date::months(tenor.months);
    new_date = date::sys_days(new_date) + date::days(tenor.days) + date::days(7 * tenor.weeks);
    return Calendar::apply_bdc(new_date, cal, bdc);
};

Tenor Tenor::operator+(const Tenor &other) const
{
    Tenor result(value);

    result.days = days + other.days;
    result.weeks = weeks + other.weeks;
    result.months = months + other.months;
    result.years = years + other.years;

    return result;
}

Tenor Tenor::operator-(const Tenor &other) const
{
    Tenor result(value);

    result.days = days - other.days;
    result.weeks = weeks - other.weeks;
    result.months = months - other.months;
    result.years = years - other.years;

    return result;
}

Tenor Tenor::operator*(int scalar) const
{
    Tenor result(value);

    result.days = days * scalar;
    result.weeks = weeks * scalar;
    result.months = months * scalar;
    result.years = years * scalar;

    return result;
}

bool Tenor::operator<(const Tenor &other) const
{
    // Calculate the total duration in days for both Tenor objects
    int totalDaysThis = days + weeks * 7 + months * 30 + years * 365;
    int totalDaysOther = other.days + other.weeks * 7 + other.months * 30 + other.years * 365;

    // Compare based on total duration in days
    return totalDaysThis < totalDaysOther;
}