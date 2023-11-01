#include <vector>
#include "../date/date.h"
#include "../date/tenor.h"
#include "../date/calendar.h"
#include "schedules.h"

using namespace std;
using namespace date;
using namespace Calendar;

SimpleSchedule Schedules::simple_schedule(const date::year_month_day &start_date, const date::year_month_day &end_date, const Tenor &frequency, const BusinessDayConvention &bdc, const DayCountMethod &dcm, const HolidayCalendar &cal)
{
    SimpleSchedule schedule;
    date::year_month_day key_date = start_date;
    int count = 1;
    while (key_date < end_date)
    {
        date::year_month_day next_key_date = add_tenor(start_date, frequency * count, cal, BusinessDayConvention::NO_ADJ);
        date::year_month_day pay_date = apply_bdc(next_key_date, cal, bdc);
        float yf = year_frac(key_date, next_key_date, dcm);
        date::days duration = date::sys_days(next_key_date) - date::sys_days(key_date);
        if (next_key_date <= end_date)
            schedule.push_back(std::make_tuple(key_date, next_key_date, duration.count(), yf, pay_date));
        key_date = next_key_date;

        count += 1;
    }
    date::year_month_day last_date = std::get<1>(schedule.back());
    if (last_date != end_date)
    {
        float yf = year_frac(last_date, end_date, dcm);
        date::days duration = date::sys_days(end_date) - date::sys_days(last_date);
        date::year_month_day pay_date = apply_bdc(end_date, cal, bdc);
        schedule.push_back(std::make_tuple(last_date, end_date, duration.count(), yf, pay_date));
    }
    return schedule;
}
