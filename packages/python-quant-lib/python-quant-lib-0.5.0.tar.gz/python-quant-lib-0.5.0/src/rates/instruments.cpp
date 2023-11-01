#include "../core/context.h"
#include "../core/solvers.h"
#include "instruments.h"
#include <vector>
#include "../date/date.h"
#include "../date/calendar.h"
#include "../core/enums.h"
#include "schedules.h"

using namespace std;
using namespace date;
using namespace LinearInstruments;
using namespace Calendar;
using namespace Enums;

// Bill

date::year_month_day DebtInstrument::get_settlement_date(const EvaluationContext &ctx)
{
    if (!this->_settlement_date.has_value() || std::get<0>(this->_settlement_date.value()) != ctx.market_date)
    {
        auto cal = ctx.get_calendar(this->calendar);
        date::year_month_day settlement_date = add_tenor(ctx.market_date, this->settlement_lag, cal, this->bdc);
        this->_settlement_date = std::make_tuple(ctx.market_date, settlement_date);
        return settlement_date;
    }
    return std::get<1>(this->_settlement_date.value());
};

SimpleSchedule Bill::schedule(const EvaluationContext &ctx)
{
    date::year_month_day settlement_date = this->get_settlement_date(ctx);
    SimpleSchedule schedule;
    date::year_month_day ref_date = settlement_date >= this->issue_date ? settlement_date : this->issue_date;
    auto cal = ctx.get_calendar(this->calendar);
    date::year_month_day pay_date = apply_bdc(maturity_date, cal, this->bdc);
    double yf = year_frac(ref_date, this->maturity_date, this->dcm);
    date::days duration = date::sys_days(this->maturity_date) - date::sys_days(ref_date);
    schedule.push_back(std::make_tuple(ref_date, this->maturity_date, duration.count(), yf, pay_date));
    return schedule;
}

PayFlows Bill::flows(const EvaluationContext &ctx)
{
    date::year_month_day settlement_date = this->get_settlement_date(ctx);
    PayFlows flows;
    date::year_month_day ref_date = settlement_date >= this->issue_date ? settlement_date : this->issue_date;
    auto cal = ctx.get_calendar(this->calendar);
    SimpleSchedule schedule = this->schedule(ctx);
    for (const auto &entry : schedule)
    {
        date::year_month_day pay_date = std::get<4>(entry);
        double yf = year_frac(ref_date, pay_date, this->dcm);
        flows.push_back(std::make_tuple(pay_date, yf, this->notional));
    }
    return flows;
}

double Bill::price(const EvaluationContext &ctx)
{
    switch (this->quote_type)
    {
    case QuoteType::PRICE:
        return this->quote;
    case QuoteType::RATE:
        auto schedule = this->schedule(ctx);
        auto yf = std::get<3>(schedule.front());
        return 1.0 - yf * this->quote;
    }
    throw("Quote Type: " + Enums::enumToString(this->quote_type) + "not supported for Bills");
}

double Bill::discount_rate(const EvaluationContext &ctx)
{
    switch (this->quote_type)
    {
    case QuoteType::RATE:
        return this->quote;
    case QuoteType::PRICE:
        auto schedule = this->schedule(ctx);
        auto yf = std::get<3>(schedule.front());
        return (1.0 - this->quote) / (yf * this->quote);
    }
    throw("Quote Type: " + Enums::enumToString(this->quote_type) + "not supported for Bills");
}

void DebtInstrument::set_quote(const double &quote, const QuoteType &quote_type)
{
    this->quote = quote;
    this->quote_type = quote_type;
}

// Bond

SimpleSchedule Bond::_get_full_schedule(const EvaluationContext &ctx)
{
    if (!this->_full_schedule.has_value())
    {
        auto cal = ctx.get_calendar(this->calendar);
        SimpleSchedule schedule = Schedules::simple_schedule(this->dated_date, this->maturity_date, this->pay_freq, this->bdc, this->dcm, cal);
        this->_full_schedule = schedule;
        return schedule;
    }
    return this->_full_schedule.value();
}

SimpleSchedule Bond::schedule(const EvaluationContext &ctx)
{
    if (!this->_schedule.has_value() || std::get<0>(this->_schedule.value()) != ctx.market_date)
    {
        SimpleSchedule adj_schedule;
        SimpleSchedule full_schedule = this->_get_full_schedule(ctx);
        date::year_month_day settlement_date = this->get_settlement_date(ctx);
        if (settlement_date <= this->dated_date)
        {
            return full_schedule;
        }
        else if (settlement_date > this->maturity_date)
        {
            throw("Settlement Date is past Maturity");
        }
        else
        {
            for (const auto &entry : full_schedule)
            {
                date::year_month_day accrual_end = std::get<1>(entry);
                date::year_month_day accrual_start = std::get<0>(entry);
                date::year_month_day pay_date = std::get<4>(entry);
                double yf = std::get<3>(entry);
                int day_count = std::get<2>(entry);
                if (accrual_end > settlement_date)
                {
                    if (settlement_date >= accrual_start)
                        accrual_start = settlement_date;
                    double yf = year_frac(accrual_start, accrual_end, this->dcm);
                    date::days duration = date::sys_days(accrual_end) - sys_days(accrual_start);
                    day_count = duration.count();
                    adj_schedule.push_back(std::make_tuple(accrual_start, accrual_end, day_count, yf, pay_date));
                }
            }
            this->_schedule = std::make_tuple(ctx.market_date, adj_schedule);
            return adj_schedule;
        }
    }
    return std::get<1>(this->_schedule.value());
}

PayFlows Bond::flows(const EvaluationContext &ctx)
{
    if (!this->_flows.has_value() || std::get<0>(this->_flows.value()) != ctx.market_date)
    {
        SimpleSchedule schedule = this->schedule(ctx);
        PayFlows flows;
        date::year_month_day settlement_date = this->get_settlement_date(ctx);
        size_t index = 0;
        double cash_flow;
        for (const auto &entry : schedule)
        {
            date::year_month_day pay_date = std::get<4>(entry);
            double accrual_yf = std::get<3>(entry);
            double yf = year_frac(settlement_date, pay_date, this->dcm);
            if (index == 0)
            {
                cash_flow = this->notional * (this->coupon_rate + this->accrued_interests(ctx)) * accrual_yf;
            }
            else if (index == schedule.size() - 1)
            {
                cash_flow = this->notional * (1 + this->coupon_rate * accrual_yf);
            }
            else
            {
                cash_flow = this->notional * (this->coupon_rate * accrual_yf);
            }
            flows.push_back(std::make_tuple(pay_date, yf, cash_flow));
            ++index;
        }
        this->_flows = std::make_tuple(ctx.market_date, flows);
    }
    return std::get<1>(this->_flows.value());
}

double Bond::_get_accrued_interests(const EvaluationContext &ctx)
{
    if (!this->_accrued_interests.has_value() || std::get<0>(this->_accrued_interests.value()) != ctx.market_date)
    {
        date::year_month_day settlement_date = this->get_settlement_date(ctx);
        date::year_month_day prev_cpn = this->dated_date;
        SimpleSchedule inst_schedule = this->_get_full_schedule(ctx);
        for (const auto &entry : inst_schedule)
        {
            date::year_month_day key_date = std::get<0>(entry);
            if (key_date > settlement_date)
            {
                break;
            }
            prev_cpn = key_date;
        }
        double yf = year_frac(prev_cpn, settlement_date, this->dcm);
        double accrued = this->coupon_rate * yf;
        this->_accrued_interests = std::make_tuple(ctx.market_date, accrued);
        return accrued;
    }
    return std::get<1>(this->_accrued_interests.value());
}

double Bond::accrued_interests(const EvaluationContext &ctx)
{
    date::year_month_day settlement_date = this->get_settlement_date(ctx);
    date::year_month_day prev_cpn = this->dated_date;
    SimpleSchedule inst_schedule = this->_get_full_schedule(ctx);
    for (const auto &entry : inst_schedule)
    {
        date::year_month_day key_date = std::get<0>(entry);
        if (key_date > settlement_date)
        {
            break;
        }
        prev_cpn = key_date;
    }
    double yf = year_frac(prev_cpn, settlement_date, this->dcm);
    return this->coupon_rate * yf;
}

double Bond::dirty_price(const EvaluationContext &ctx)
{
    double dp;
    switch (this->quote_type)
    {
    case QuoteType::DIRTY_PRICE:
        return this->quote;
    case QuoteType::CLEAN_PRICE:
        return this->quote + this->accrued_interests(ctx);
    case QuoteType::RATE:
        return this->yield_to_dirty_price(this->quote, ctx);
    }
    throw("Quote Type: " + Enums::enumToString(this->quote_type) + "not supported for Bonds");
}

double Bond::clean_price(const EvaluationContext &ctx)
{
    double cp;
    switch (this->quote_type)
    {
    case QuoteType::DIRTY_PRICE:
        return this->quote - this->accrued_interests(ctx);
    case QuoteType::CLEAN_PRICE:
        return this->quote;
    case QuoteType::RATE:
        return this->yield_to_dirty_price(this->quote, ctx) - this->accrued_interests(ctx);
    }
    throw("Quote Type: " + Enums::enumToString(this->quote_type) + "not supported for Bonds");
}

double Bond::yield_to_dirty_price(const double &yield, const EvaluationContext &ctx)
{
    date::year_month_day settlement_date = this->get_settlement_date(ctx);
    SimpleSchedule schedule;
    double yf;
    switch (this->yield_type)
    {
    case YieldCalcType::CURRENT_YIELD:
        return (yield / this->coupon_rate) + this->accrued_interests(ctx);
    case YieldCalcType::SIMPLE_YIELD:
        yf = year_frac(settlement_date, this->maturity_date, DayCountMethod::EX_LEAP_365);
        return (this->coupon_rate + 1 / yf) / (yield + 1 / yf) + this->accrued_interests(ctx);
    case YieldCalcType::STREET:
        schedule = this->schedule(ctx);
        int periods = this->_get_yearly_payments();
        if (schedule.size() == 1)
        {
            yf = std::min(std::get<3>(schedule.back()) * periods, 1.0);
            return (1 + this->coupon_rate) / (1 + yf * yield / periods);
        }
        else
        {
            yf = std::min(std::get<3>(schedule.front()) * periods, 1.0);
            double df = 1 / (1 + yield / periods);
            int payments = schedule.size();
            double term1 = (this->coupon_rate / periods);
            double term2 = (this->coupon_rate / periods) * df;
            double term3 = (this->coupon_rate / periods) * df * df * ((1 - std::pow(df, (payments - 2))) / (1 - df));
            double term4 = std::pow(df, (payments - 1));
            return std::pow(df, yf) * (term1 + term2 + term3 + term4);
        }
    }
    throw("Yield Calculation: " + enumToString(this->yield_type) + " is not supported");
}

double Bond::dirty_price_to_yield(const double &dp, const EvaluationContext &ctx)
{
    double yield = Solvers::new_raph_solve(
        [ctx, this](double x)
        {
            return this->yield_to_dirty_price(x, ctx);
        },
        dp);
    return yield;
}

double Bond::yield(const EvaluationContext &ctx)
{
    double y;
    switch (this->quote_type)
    {
    case QuoteType::DIRTY_PRICE:
        return this->dirty_price_to_yield(this->quote, ctx);
    case QuoteType::CLEAN_PRICE:
        return this->dirty_price_to_yield(this->quote + this->accrued_interests(ctx), ctx);
    case QuoteType::RATE:
        return this->quote;
    }
    throw("Quote Type: " + Enums::enumToString(this->quote_type) + "not supported for Bonds");
}

int Bond::_get_yearly_payments()
{
    if (!this->_yearly_payments.has_value())
    {
        if (this->pay_freq.years == 1)
        {
            this->_yearly_payments = 1;
            return this->_yearly_payments.value();
        }
        else if (this->pay_freq.years == 0 && this->pay_freq.months <= 12 && this->pay_freq.weeks == 0 && this->pay_freq.days == 0)
        {
            this->_yearly_payments = 12 / this->pay_freq.months;
        }
        else
        {
            throw("PayFreq is not supported for Yield Componding computations");
        }
    }
    return this->_yearly_payments.value();
}
