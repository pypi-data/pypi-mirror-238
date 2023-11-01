#ifndef SCHEDULES_H
#define SCHEDULES_H

#include <vector>
#include "../date/date.h"
#include "../date/tenor.h"
#include "../date/calendar.h"

using namespace std;
using namespace date;
using namespace Calendar;

using SimpleSchedule = std::vector<std::tuple<date::year_month_day, date::year_month_day, int, double, date::year_month_day>>;

namespace Schedules
{

    SimpleSchedule simple_schedule(const date::year_month_day &start_date, const date::year_month_day &end_date, const Tenor &frequency, const BusinessDayConvention &bdc, const DayCountMethod &dcm, const HolidayCalendar &cal);

}

#endif // SCHEDULES_H