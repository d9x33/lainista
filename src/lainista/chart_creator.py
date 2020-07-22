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


# takes the data and returns a list from given indices
def get_chart_data_with_indices(data, start, end) -> list:
    dates = [x["y"] for x in data][start:end]
    values = [x["a"] for x in data][start:end]

    #[dates] = (list(map(lambda x: x["y"], data))[start:end],)
    #[values] = (list(map(lambda x: x["a"], data))[start:end],)

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
    google_chart_data = google_main()[1]["chart_data"]

    import pdb; pdb.set_trace()
    create_and_save_chart(google_chart_data["today"][0][""], 20, "daily_google_chart.png")
    create_and_save_chart(google_chart_data["today"][1]["images"], 20, "daily_google_images_chart.png")
    create_and_save_chart(google_chart_data["today"][2]["news"], 20, "daily_google_news_chart.png")
    create_and_save_chart(google_chart_data["today"][3]["youtube"], 20, "daily_google_youtube_chart.png")
    create_and_save_chart(google_chart_data["today"][4]["news"], 20, "daily_google_news_chart.png")

    create_and_save_chart(google_chart_data["week"][0][""], 20, "weekly_google_chart.png")
    create_and_save_chart(google_chart_data["week"][1]["images"], 20, "weekly_google_images_chart.png")
    create_and_save_chart(google_chart_data["week"][2]["news"], 20, "weekly_google_news_chart.png")
    create_and_save_chart(google_chart_data["week"][3]["youtube"], 20, "weekly_google_youtube_chart.png")
    create_and_save_chart(google_chart_data["week"][4]["news"], 20, "weekly_google_news_chart.png")


    daily_google_data = google_chart_data["today"][0]["''"]
    daily_images_data = google_chart_data["today"]["images"]
    daily_news_data = google_chart_data["today"]["news"]
    daily_youtube_data = google_chart_data["today"]["youtube"]
    daily_froogle_data = google_chart_data["today"]["froogle"]

    weekly_google_data = google_chart_data["week"]["''"]
    weekly_images_data = google_chart_data["week"]["images"]
    weekly_news_data = google_chart_data["week"]["news"]
    weekly_youtube_data = google_chart_data["week"]["youtube"]
    weekly_froogle_data = google_chart_data["week"]["froogle"]

    monthly_google_data = google_chart_data["month"]["''"]
    monthly_images_data = google_chart_data["month"]["images"]
    monthly_news_data = google_chart_data["month"]["news"]
    monthly_youtube_data = google_chart_data["month"]["youtube"]
    monthly_froogle_data = google_chart_data["month"]["froogle"]


    yearly_google_data = google_chart_data["year"]["''"]
    yearly_images_data = google_chart_data["year"]["images"]
    yearly_news_data = google_chart_data["year"]["news"]
    yearly_youtube_data = google_chart_data["year"]["youtube"]
    yearly_froogle_data = google_chart_data["year"]["froogle"]



def main():
    check_if_plots_dir_exists_and_create(CHART_DIR)

    get_and_plot_reddit_chart_data()
    get_and_plot_google_chart_data()


if __name__ == "__main__":
    main()
