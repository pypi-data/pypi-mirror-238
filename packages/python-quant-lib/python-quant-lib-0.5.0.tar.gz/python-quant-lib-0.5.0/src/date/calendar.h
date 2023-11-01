#ifndef CALENDAR_H
#define CALENDAR_H

#include "date.h"

using namespace std;

namespace Calendar
{

    enum struct DayCountMethod
    {
        ACT_ACT,
        ACT_360,
        ACT_365,
        ACT_365F,
        EX_LEAP_365,
    };

    enum struct BusinessDayConvention
    {
        NO_ADJ,
        FOLLOWING,
        PRECEEDING,
        MODIFIED_FOLLOWING,
        END_OF_MONTH,
        END_OF_MONTH_ADJ
    };

    struct HolidayCalendar
    {
        std::string name;
        std::vector<date::year_month_day> holidays;
        std::vector<date::weekday> week_ends;
        HolidayCalendar() : name{"NO_HOL"}, week_ends{{date::Saturday, date::Sunday}} {}
        HolidayCalendar(std::string name_, std::vector<date::year_month_day> holidays_, std::vector<date::weekday> week_ends_) : name{name_}, holidays{holidays_}, week_ends{week_ends_} {}

        bool is_bday(const date::year_month_day &date) const;
    };

    // BDC
    date::year_month_day modified_following(const date::year_month_day &date, const HolidayCalendar &cal);
    date::year_month_day preceeding(const date::year_month_day &date, const HolidayCalendar &cal);
    date::year_month_day modified_following(const date::year_month_day &date, const HolidayCalendar &cal);
    date::year_month_day apply_bdc(const date::year_month_day &date, const HolidayCalendar &cal, const BusinessDayConvention &bdc);
    date::year_month_day following(const date::year_month_day &date, const HolidayCalendar &cal);

    // DCM
    double year_frac(date::year_month_day d1, date::year_month_day d2, DayCountMethod cdm);

}

#endif // CALENDAR_H