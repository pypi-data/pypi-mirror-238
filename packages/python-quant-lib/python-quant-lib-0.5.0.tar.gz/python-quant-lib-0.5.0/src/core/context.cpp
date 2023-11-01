#include "context.h"
#include <map>
#include <vector>
#include "../date/date.h"
#include "../date/calendar.h"
#include "configs.h"

using namespace std;

Calendar::HolidayCalendar EvaluationContext::get_calendar(const std::string &code) const
{
    auto cal = calendars.find(code);
    if (cal == calendars.end())
    {
        throw("Could not find calendar " + code + " in calendar map");
    }
    return cal->second;
};

CalibrationConfig EvaluationContext::get_calibration_config() const
{
    return this->calibration_config;
}

std::vector<Calendar::HolidayCalendar> EvaluationContext::get_calendars(const std::vector<std::string> &codes) const
{
    std::vector<Calendar::HolidayCalendar> cals;
    for (const std::string &code : codes)
    {
        cals.emplace_back(get_calendar(code));
    };
    return cals;
}
void EvaluationContext::set_calendars(const std::map<std::string, Calendar::HolidayCalendar> &cals)
{
    for (const auto &entry : cals)
    {
        calendars[entry.first] = entry.second;
    }
}

void EvaluationContext::set_calibration_config(const CalibrationConfig &config)
{
    this->calibration_config = config;
}