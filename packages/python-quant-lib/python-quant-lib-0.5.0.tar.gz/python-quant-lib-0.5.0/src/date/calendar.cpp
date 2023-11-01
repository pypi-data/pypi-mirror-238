#include "calendar.h"
#include "date.h"
#include "../core/enums.h"

using namespace std;

bool Calendar::HolidayCalendar::is_bday(const date::year_month_day &date) const
{
    date::weekday wd = date::weekday(date::sys_days(date));
    if (std::find(this->week_ends.begin(), this->week_ends.end(), wd) != this->week_ends.end())
    {
        return false;
    }
    else if (std::find(this->holidays.begin(), this->holidays.end(), date) != this->holidays.end())
    {
        return false;
    }
    else
    {
        return true;
    }
};

date::year_month_day Calendar::following(const date::year_month_day &date, const Calendar::HolidayCalendar &cal)
{
    date::year_month_day adjusted_date = date;
    while (cal.is_bday(adjusted_date) == false)
    {
        adjusted_date = date::sys_days(adjusted_date) + date::days(1);
    }
    return adjusted_date;
};

date::year_month_day Calendar::preceeding(const date::year_month_day &date, const Calendar::HolidayCalendar &cal)
{
    date::year_month_day adjusted_date = date;
    while (cal.is_bday(adjusted_date) == false)
    {
        adjusted_date = date::sys_days(adjusted_date) - date::days(1);
    }
    return adjusted_date;
};

date::year_month_day Calendar::modified_following(const date::year_month_day &date, const Calendar::HolidayCalendar &cal)
{
    date::year_month_day adjusted_date = following(date, cal);
    if (adjusted_date.month() != date.month())
    {
        adjusted_date = preceeding(date, cal);
    }
    return adjusted_date;
};

date::year_month_day Calendar::apply_bdc(const date::year_month_day &date, const Calendar::HolidayCalendar &cal, const Calendar::BusinessDayConvention &bdc)
{
    const bool is_bday = cal.is_bday(date);
    if (is_bday)
    {
        return date;
    }
    else
    {
        switch (bdc)
        {
        case Calendar::BusinessDayConvention::NO_ADJ:
            return date;
        case Calendar::BusinessDayConvention::FOLLOWING:
            return following(date, cal);
        case Calendar::BusinessDayConvention::PRECEEDING:
            return preceeding(date, cal);
        case Calendar::BusinessDayConvention::MODIFIED_FOLLOWING:
            return modified_following(date, cal);
        }
        throw std::invalid_argument("Unsupported Business Day Convention: " + Enums::enumToString(bdc));
    }
    return date;
};

double Calendar::year_frac(date::year_month_day d1, date::year_month_day d2, Calendar::DayCountMethod cdm)
{
    double yf;
    bool is_leap;
    int year;
    double daycount;
    date::days duration = date::sys_days(d2) - date::sys_days(d1);
    switch (cdm)
    {
    case Calendar::DayCountMethod::ACT_360:
        daycount = 360.0;
        yf = duration.count() / daycount;
        return yf;
    case Calendar::DayCountMethod::ACT_365F:
        daycount = 365.0;
        yf = duration.count() / daycount;
        return yf;
    case Calendar::DayCountMethod::ACT_365:
        // TODO: handle case of multi years year frac
        year = static_cast<int>(d2.year());
        is_leap = (year % 4 == 0) && (year % 100 != 0 || year % 400 == 0);
        daycount = is_leap ? 366.0 : 365.0;
        yf = duration.count() / daycount;
        return yf;
    case Calendar::DayCountMethod::EX_LEAP_365:
        // For computing Simple Yield year fracts
        // Computes actual day over 365 excluding 29th of Feb
        int to_sub = 0;
        int d1_year = static_cast<int>(d1.year());
        int d2_year = static_cast<int>(d2.year());
        date::year_month_day start(d1.year(), date::month(2), date::day(29));
        bool is_d1_leap = (d1_year % 4 == 0) && (d1_year % 100 != 0 || d1_year % 400 == 0);
        if (d1 <= start && is_d1_leap)
            to_sub += 1;
        if (d1_year != d2_year)
        {
            int start_year = d1_year + 1;
            int finish_year = d2_year - 1;
            date::year_month_day end(d2.year(), date::month(2), date::day(29));
            bool is_d2_leap = (d2_year % 4 == 0) && (d1_year % 100 != 0 || d2_year % 400 == 0);
            if (d2 >= end && is_d2_leap)
                to_sub += 1;
            while (start_year <= finish_year)
            {
                is_leap = (start_year % 4 == 0) && (start_year % 100 != 0 || start_year % 400 == 0);
                if (is_leap)
                    to_sub += 1;
                start_year += 1;
            }
        }
        daycount = 365.0;
        yf = (duration.count() - to_sub) / daycount;
        return yf;
    }
    throw std::invalid_argument("Unsupported Day Count Method: " + Enums::enumToString(cdm));
}
