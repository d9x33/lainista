from reddit import main as reddit_main
from google_trends import main as google_main
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

CHART_DIR = os.path.join(os.getcwd(), "../../plots")

# checks if plots dir exists, if not, creates it
def check_if_plots_dir_exists_and_create(path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


# plots the data and saves it
def create_and_save_chart(data, x_tick_interval, file_name) -> None:
    fig, ax = plt.subplots()
    plt.plot(data["dates"], data["values"])
    plt.setp(
        ax.get_xticklabels(),
        rotation=30,
        horizontalalignment="right",
        fontsize="x-small",
    )
    ax.set_xticks(data["dates"][::x_tick_interval])
    plt.savefig("{}/{}".format(CHART_DIR, file_name))


# helper func to iterate over create_and_save for google stuff because it would become too repetitive
def google_plotter_iterator(data, tf, tf_name, gprops) -> None:
    for idx, gprop in enumerate(gprops):
        create_and_save_chart(data[tf][idx][gprop], 5, "google_{}_{}_chart.png".format(tf_name, gprop))

# takes the data and returns a list from given indices
def get_chart_data_with_indices(data, start, end) -> list:
    dates = [x["y"] for x in data][start:end]
    values = [x["a"] for x in data][start:end]

    return {"dates": dates, "values": values}


# get data from reddit and plot it
def get_and_plot_reddit_chart_data() -> None:
    reddit_chart_data = reddit_main()["chart_data"]

    weekly_chart_data = get_chart_data_with_indices(reddit_chart_data, -8, -1)
    monthly_chart_data = get_chart_data_with_indices(reddit_chart_data, -30, -1)
    yearly_chart_data = get_chart_data_with_indices(reddit_chart_data, -366, -1)
    # here 1 stands for the beginning of the list, couldn't find a better way to write it
    entire_timeline_chart_data = get_chart_data_with_indices(reddit_chart_data, 1, -1)

    create_and_save_chart(weekly_chart_data, 1, "reddit_weekly_chart.png")
    create_and_save_chart(monthly_chart_data, 2, "reddit_monthly_chart.png")
    create_and_save_chart(yearly_chart_data, 20, "reddit_yearly_chart.png")
    create_and_save_chart(entire_timeline_chart_data, 200, "reddit_entire_chart.png")

# get data from google and plot it
def get_and_plot_google_chart_data() -> None:
    GPROPS = ["", "images", "news", "youtube", "froogle"]

    google_chart_data = google_main()[1]["chart_data"]

    google_plotter_iterator(google_chart_data, "today", "daily", GPROPS)
    google_plotter_iterator(google_chart_data, "week", "weekly", GPROPS)
    google_plotter_iterator(google_chart_data, "month", "monthly", GPROPS)
    google_plotter_iterator(google_chart_data, "year", "yearly", GPROPS)


def main():
    check_if_plots_dir_exists_and_create(CHART_DIR)

    get_and_plot_reddit_chart_data()
    get_and_plot_google_chart_data()


if __name__ == "__main__":
    main()
