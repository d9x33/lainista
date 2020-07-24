from .reddit_scraper import main as reddit_main
from .google_scraper import main as google_main
from .google_scraper import GPROPS
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# defaults to the src/static/plot folder inside the react directory.
GOOGLE_CHART_DIR = os.path.join(os.getcwd(), "../client/src/static/plots/google")
REDDIT_CHART_DIR = os.path.join(os.getcwd(), "../client/src/static/plots/reddit")


# plots the data and saves it
def create_and_save_chart(data, x_tick_interval, file_name, target_dir) -> None:
    _, ax = plt.subplots()
    plt.plot(data["dates"], data["values"])
    plt.setp(
        ax.get_xticklabels(),
        rotation=30,
        horizontalalignment="right",
        fontsize="x-small",
    )
    ax.set_xticks(data["dates"][::x_tick_interval])
    plt.savefig("{}/{}".format(target_dir, file_name))


# helper func to iterate over create_and_save for google stuff because it would become too repetitive
def google_plotter_iterator(data, tf, tf_name, gprops) -> None:
    for idx, gprop in enumerate(gprops):
        create_and_save_chart(
            data[tf][idx][gprop], 5, "google_{}_{}_chart.png".format(tf_name, gprop), GOOGLE_CHART_DIR)


# takes the data and returns a list from given indices
def get_chart_data_with_indices(data, start, end) -> list:
    dates = [x["y"] for x in data][start:end]
    values = [x["a"] for x in data][start:end]

    return {"dates": dates, "values": values}


# get data from reddit and plot it
def plot_reddit_chart_data(data) -> None:
    weekly_chart_data = get_chart_data_with_indices(data, -8, -1)
    monthly_chart_data = get_chart_data_with_indices(data, -30, -1)
    yearly_chart_data = get_chart_data_with_indices(data, -366, -1)
    entire_timeline_chart_data = get_chart_data_with_indices(data, 1, -1)

    create_and_save_chart(weekly_chart_data, 1, "reddit_weekly_chart.png", REDDIT_CHART_DIR)
    create_and_save_chart(monthly_chart_data, 2, "reddit_monthly_chart.png", REDDIT_CHART_DIR)
    create_and_save_chart(yearly_chart_data, 20, "reddit_yearly_chart.png", REDDIT_CHART_DIR)
    create_and_save_chart(entire_timeline_chart_data,
                          200, "reddit_entire_chart.png", REDDIT_CHART_DIR)


# get data from google and plot it
def plot_google_chart_data(data) -> None:
    google_plotter_iterator(data, "today", "daily", GPROPS)
    google_plotter_iterator(data, "week", "weekly", GPROPS)
    google_plotter_iterator(data, "month", "monthly", GPROPS)
    google_plotter_iterator(data, "year", "yearly", GPROPS)


def main(google_data, reddit_data):
    if not os.path.exists(REDDIT_CHART_DIR):
        os.makedirs(REDDIT_CHART_DIR)

    if not os.path.exists(GOOGLE_CHART_DIR):
        os.makedirs(GOOGLE_CHART_DIR)

    plot_google_chart_data(google_data)
    plot_reddit_chart_data(reddit_data)

