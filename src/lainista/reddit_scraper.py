import requests
from bs4 import BeautifulSoup
import regex as re
import json

SUB_GROWTH_REGEX = "(?<=element: 'subscriber-growth',.*data: \[)(.+?)(?=\])"
TOTAL_SUB_REGEX = "(?<=element: 'total-subscribers',.*data: \[)(.+?)(?=\])"
RANK_REGEX = "(?<=rankData.*\[)(.+?)(?=\])"

# matches a regex inside the soup and returns it while removing whitespace
def search_by_regex(regexp, soup) -> list:
    return re.search(regexp, soup).group(0).replace(" ", "")


# get soup from request, return it
def get_soup(url) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url).text, "lxml")


# find all <script> tags within the soup, returns a string containing them
def get_script_tags(soup) -> str:
    return str.join(" ", str(soup.find_all("script")).splitlines())


# deserialize the parsed data and format it to be a proper json, returns a list type with json data
def deserialize(parsed_data) -> list:
    jsonized = parsed_data.replace("'", '"').replace("y", '"y"').replace("a", '"a"')
    return json.loads("[{}]".format(jsonized))


# helper func for determining lain's mood and the according percentages from the data, returns a dict with corresponding data
def mood_and_percentage_change_from_first_and_second(first_half, second_half) -> dict:
    percent_change = (second_half - first_half) / first_half * 100

    if second_half >= first_half:
        return {"current_mood": 1, "percentage_change": percent_change}
    return {"current_mood": -1, "percentage_change": percent_change}


# get difference from last day compared to the day before that
def get_daily(data) -> dict:
    first_half, second_half = data[-1]["a"], data[-2]["a"]

    return mood_and_percentage_change_from_first_and_second(first_half, second_half)


# func that takes start and end as indices which represent days, for example
# -30 as start and -15 as end would return the comparison from the last month
def get_with_indices(data, start, end) -> dict:
    first_half, second_half = (
        sum([x["a"] for x in data][start:end]),
        sum([x["a"] for x in data][end:]),
    )

    return mood_and_percentage_change_from_first_and_second(first_half, second_half)


def main():

    soup = get_soup("https://redditmetrics.com/r/Lain")

    script_tags = get_script_tags(soup)

    sub_growth_data = deserialize(search_by_regex(SUB_GROWTH_REGEX, script_tags))
    total_sub_data = deserialize(search_by_regex(TOTAL_SUB_REGEX, script_tags))
    rank_data = deserialize(search_by_regex(RANK_REGEX, script_tags))

    daily_data = get_daily(total_sub_data)
    weekly_data = get_with_indices(total_sub_data, -8, -4)
    monthly_data = get_with_indices(total_sub_data, -30, -15)
    yearly_data = get_with_indices(total_sub_data, -366, -183)

    return {
        "mood": {
            "today": daily_data["current_mood"],
            "week": weekly_data["current_mood"],
            "month": monthly_data["current_mood"],
            "year": yearly_data["current_mood"],
        },
        "percentage_change": {
            "today": daily_data["percentage_change"],
            "week": weekly_data["percentage_change"],
            "month": monthly_data["percentage_change"],
            "year": yearly_data["percentage_change"],
        },
        "chart_data": total_sub_data,
    }


if __name__ == "__main__":
    main()
