from pytrends.request import TrendReq
from itertools import repeat

# makes a request and returns dates and values for a specific gprop
def pytrends_make_req_chart(kw_list, tf, gprop) -> dict:
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(kw_list, cat=0, timeframe=tf, geo="", gprop=gprop)

    iot = pytrends.interest_over_time()

    iot["value"] = iot["lain"] + iot["sel"] + iot["serial experiments lain"]

    iot.reset_index(inplace=True)

    return {"dates": list(iot["date"]), "values": list(iot["value"])}


# returns chart data in the format of values and dates in order to plot it later.
def pytrends_get_chart_data(kw_list, tf, gprops) -> list:
    pytrends_data = list(
        map(
            pytrends_make_req_chart,
            repeat(kw_list, len(gprops)),
            repeat(tf, len(gprops)),
            gprops,
        )
    )

    values = [x["values"] for x in pytrends_data]
    unformatted_dates = [x["dates"] for x in pytrends_data]
    print([[x.strftime("%d-%m-%Y")]  for x in unformatted_dates])

    final_data = [
        {x: {"dates": pytrends_data[i]["dates"], "values": pytrends_data[i]["values"]}}
        for i, x in enumerate(gprops)
    ]
    # values = list(map(sum, zip(*list(map(lambda x: x["values"], pytrends_data)))))
    # dates = list(map(lambda x: x.strftime("%d-%m-%Y"), pytrends_data[0]["dates"]))

    # return {"dates": dates, "values": values}
   
    return final_data


# make pytrends request, returns a pair sum of first and second half
def pytrends_make_req(kw_list, tf, gprop) -> list:
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(kw_list, cat=0, timeframe=tf, geo="", gprop=gprop)

    iot = pytrends.interest_over_time()

    sum_of_1st_half = iot.iloc[: int(len(iot) / 2)].sum(numeric_only=True).sum()
    sum_of_2nd_half = iot.iloc[int(len(iot) / 2) :].sum(numeric_only=True).sum()

    return [sum_of_1st_half, sum_of_2nd_half]


# sum up and format the data from pytrends request FOR EACH GPROP, returns a pair with the sum of first and second half for all gprops
def pytrends_get_data(kw_list, gprops, tf) -> list:
    pytrends_data = list(
        map(
            pytrends_make_req,
            repeat(kw_list, len(gprops)),
            repeat(tf, len(gprops)),
            gprops,
        )
    )

    final_sum_of_1st_half = sum([x[0] for x in pytrends_data])
    final_sum_of_2nd_half = sum(x[1] for x in pytrends_data)

    return [final_sum_of_1st_half, final_sum_of_2nd_half]


# helper func for determining lain's mood and the according percentages from the data, returns a dict with corresponding data
def check_mood_and_percentage_change(data) -> dict:
    first_half, second_half = data[0], data[1]

    percent_change = (second_half - first_half) / first_half * 100

    if second_half >= first_half:
        return {"current_mood": 1, "percentage_change": percent_change}
    return {"current_mood": -1, "percentage_change": percent_change}


# wrapper func to map and analyze all the data and return the value, returns a dict with formatted mood/percentage change data
def analyze_data(daily, weekly, monthly, yearly) -> dict:
    checked_data = list(
        map(check_mood_and_percentage_change, [daily, weekly, monthly, yearly])
    )

    mood_today, mood_week, mood_month, mood_year = [
        x["current_mood"] for x in checked_data
    ]
    (
        percentage_change_today,
        percentage_change_week,
        percentage_change_month,
        percentage_change_year,
    ) = [x["percentage_change"] for x in checked_data]

    return {
        "mood": {
            "today": mood_today,
            "week": mood_week,
            "month": mood_month,
            "year": mood_year,
        },
        "percentage_change": {
            "today": percentage_change_today,
            "week": percentage_change_week,
            "month": percentage_change_month,
            "year": percentage_change_year,
        },
    }


def main():
    KW_LIST = ["lain", "sel", "serial experiments lain"]
    GPROPS = ["", "images", "news", "youtube", "froogle"]

    daily_data = pytrends_get_data(KW_LIST, GPROPS, "now 1-d")
    weekly_data = pytrends_get_data(KW_LIST, GPROPS, "now 7-d")
    monthly_data = pytrends_get_data(KW_LIST, GPROPS, "today 1-m")
    # 1-y instead of 12-m throws an error, don't ask me why
    yearly_data = pytrends_get_data(KW_LIST, GPROPS, "today 12-m")

    daily_chart_data = pytrends_get_chart_data(KW_LIST, "now 1-d", GPROPS)
    weekly_chart_data = pytrends_get_chart_data(KW_LIST, "now 7-d", GPROPS)
    monthly_chart_data = pytrends_get_chart_data(KW_LIST, "today 1-m", GPROPS)
    yearly_chart_data = pytrends_get_chart_data(KW_LIST, "today 12-m", GPROPS)

    analyzed_data = analyze_data(daily_data, weekly_data, monthly_data, yearly_data)

    return [
        analyzed_data,
        {
            "chart_data": {
                "today": daily_chart_data,
                "week": weekly_chart_data,
                "month": monthly_chart_data,
                "year": yearly_chart_data,
            }
        },
    ]


if __name__ == "__main__":
    main()
