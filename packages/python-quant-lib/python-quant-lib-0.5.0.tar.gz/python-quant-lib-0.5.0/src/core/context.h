#ifndef CONTEXT_H
#define CONTEXT_H

#include <map>
#include <vector>
#include <chrono>
#include "../date/date.h"
#include "../date/calendar.h"
#include "configs.h"

using namespace std;

struct EvaluationContext
{
    date::year_month_day market_date;
    // Calendars
    Calendar::HolidayCalendar get_calendar(const std::string &code) const;
    CalibrationConfig get_calibration_config() const;
    std::vector<Calendar::HolidayCalendar> get_calendars(const std::vector<std::string> &codes) const;
    void set_calendars(const std::map<std::string, Calendar::HolidayCalendar> &calendars);
    void set_calibration_config(const CalibrationConfig &config);

    EvaluationContext()
    {
        auto today = std::chrono::system_clock::now();
        auto dp = date::floor<date::days>(today);
        market_date = date::year_month_day{dp};
        calibration_config = CalibrationConfig();
    };
    EvaluationContext(const date::year_month_day &market_date, const CalibrationConfig &calib_config = CalibrationConfig()) : market_date{market_date}, calibration_config{calib_config} {};
    EvaluationContext(const EvaluationContext &ctx)
    {
        market_date = ctx.market_date;
        calendars = ctx.calendars;
        calibration_config = ctx.calibration_config;
    }

private:
    std::map<std::string, Calendar::HolidayCalendar> calendars;
    CalibrationConfig calibration_config;
};

#endif // CONTEXT_H