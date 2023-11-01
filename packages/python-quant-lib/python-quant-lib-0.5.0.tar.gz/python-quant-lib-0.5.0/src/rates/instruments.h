#ifndef INSTRUMENTS_H
#define INSTRUMENTS_H

#include "../date/date.h"
#include "../date/calendar.h"
#include "../date/tenor.h"
#include "../core/context.h"
#include "schedules.h"
#include <optional>
#include <string>

using namespace std;
using namespace date;
using namespace Calendar;

enum struct QuoteType
{
    RATE,
    SPREAD,
    PRICE,
    CLEAN_PRICE,
    DIRTY_PRICE
};

enum struct YieldCalcType
{
    CURRENT_YIELD,
    SIMPLE_YIELD,
    REDEMPTION,
    US_TREASURY,
    STREET,

};

using PayFlows = std::vector<std::tuple<date::year_month_day, double, double>>;

namespace LinearInstruments
{
    class DebtInstrument
    {
    protected:
        std::string issuer;
        std::string currency;
        date::year_month_day issue_date;
        date::year_month_day maturity_date;
        Calendar::BusinessDayConvention bdc;
        Calendar::DayCountMethod dcm;
        std::string calendar;
        Tenor settlement_lag;
        double quote;
        QuoteType quote_type;
        double notional;

        std::optional<std::tuple<date::year_month_day, date::year_month_day>> _settlement_date;

    public:
        DebtInstrument(const std::string &issuer,
                       const std::string &currency,
                       const date::year_month_day &issue_date,
                       const date::year_month_day &maturity_date,
                       const Calendar::BusinessDayConvention &bdc,
                       const Calendar::DayCountMethod &dcm,
                       const std::string &calendar,
                       const double &quote,
                       const QuoteType &quote_type,
                       const double notional,
                       const Tenor &settlement_lag) : issuer{issuer}, currency{currency}, issue_date{issue_date}, maturity_date{maturity_date}, bdc{bdc}, dcm{dcm}, calendar{calendar}, quote{quote}, quote_type{quote_type}, settlement_lag{settlement_lag}, notional{notional} {};

        virtual SimpleSchedule schedule(const EvaluationContext &ctx) = 0;
        virtual PayFlows flows(const EvaluationContext &ctx) = 0;

        // Getters
        const std::string &get_issuer() const { return issuer; };
        const std::string &get_currency() const { return currency; };
        const date::year_month_day &get_issue_date() const { return issue_date; };
        const date::year_month_day &get_maturity_date() const { return maturity_date; };
        const Calendar::BusinessDayConvention &get_bdc() const { return bdc; };
        const Calendar::DayCountMethod &get_dcm() const { return dcm; };
        const std::string &get_calendar() const { return calendar; };
        const double &get_quote() const { return quote; };
        const QuoteType &get_quote_type() const { return quote_type; };
        const Tenor &get_settlement_lag() const { return settlement_lag; };
        date::year_month_day get_settlement_date(const EvaluationContext &ctx);

        // Setters
        void set_quote(const double &quote, const QuoteType &quote_type);
    };

    class Bill : public DebtInstrument
    {
    public:
        Bill(const std::string &issuer,
             const std::string &currency,
             const date::year_month_day &issue_date,
             const date::year_month_day &maturity_date,
             const Calendar::BusinessDayConvention &bdc,
             const Calendar::DayCountMethod &dcm,
             const std::string &calendar,
             const double &quote,
             const QuoteType &quote_type,
             const double notional,
             const Tenor &settlement_lag) : DebtInstrument(issuer, currency, issue_date, maturity_date, bdc, dcm, calendar, quote, quote_type, notional, settlement_lag){};

        SimpleSchedule schedule(const EvaluationContext &ctx) override;
        PayFlows flows(const EvaluationContext &ctx) override;
        double price(const EvaluationContext &ctx);
        double discount_rate(const EvaluationContext &ctx);
    };

    class Bond : public DebtInstrument
    {
    protected:
        date::year_month_day dated_date;
        double coupon_rate;
        Tenor pay_freq;
        YieldCalcType yield_type;

        std::optional<SimpleSchedule> _full_schedule;
        std::optional<std::tuple<date::year_month_day, SimpleSchedule>> _schedule;
        std::optional<std::tuple<date::year_month_day, double>> _accrued_interests;
        std::optional<int> _yearly_payments;
        std::optional<std::tuple<date::year_month_day, PayFlows>> _flows;

        SimpleSchedule _get_full_schedule(const EvaluationContext &ctx);
        double _get_accrued_interests(const EvaluationContext &ctx);
        int _get_yearly_payments();

        double dirty_price_to_yield(const double &dp, const EvaluationContext &ctx);
        double yield_to_dirty_price(const double &yield, const EvaluationContext &ctx);

    public:
        Bond(const std::string &issuer,
             const std::string &currency,
             const date::year_month_day &issue_date,
             const date::year_month_day &dated_date,
             const date::year_month_day &maturity_date,
             const Calendar::BusinessDayConvention &bdc,
             const Calendar::DayCountMethod &dcm,
             const std::string &calendar,
             const double &quote,
             const double &coupon_rate,
             const QuoteType &quote_type,
             const double notional,
             const Tenor &settlement_lag,
             const Tenor &pay_freq,
             const YieldCalcType yield_type) : DebtInstrument(issuer, currency, issue_date, maturity_date, bdc, dcm, calendar, quote, quote_type, notional, settlement_lag), dated_date{dated_date}, coupon_rate{coupon_rate}, pay_freq{pay_freq}, yield_type{yield_type} {};

        SimpleSchedule schedule(const EvaluationContext &ctx) override;
        PayFlows flows(const EvaluationContext &ctx) override;
        double accrued_interests(const EvaluationContext &ctx);
        double clean_price(const EvaluationContext &ctx);
        double dirty_price(const EvaluationContext &ctx);
        double yield(const EvaluationContext &ctx);

        // Getters
        const date::year_month_day &get_dated_date() const { return dated_date; };
        const double &get_coupon_rate() const { return coupon_rate; };
        const Tenor &get_pay_freq() const { return pay_freq; };
        const YieldCalcType &get_yield_type() const { return yield_type; };
    };

};

#endif // INSTRUMENTS_H