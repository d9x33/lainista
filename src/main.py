from lainista.google_scraper import main as google_main
from lainista.plotter import main as plotter_main
from lainista.reddit_scraper import main as reddit_main
from rmwrapper import RedditMetricsWrapper
import json
import os

REDDIT_JSON_DIR = "../client/src/components/data"
GOOGLE_JSON_DIR = "../client/src/components/data"


def get_data() -> dict:
    google_data = google_main()
    reddit_data = reddit_main()

    return {"google": google_data, "reddit": reddit_data}



def save_google_data_as_json(data) -> None:
    with open("{}/{}".format(GOOGLE_JSON_DIR, "google_data.json"), "w+") as f:
        json.dump(data["google"][0], f)


def save_reddit_data_as_json(data) -> None:
    with open("{}/{}".format(REDDIT_JSON_DIR, "reddit_data.json"), "w+") as f:
        json.dump(
            {
                "mood": data["reddit"]["mood"],
                "percentage_change": (data["reddit"]["percentage_change"]),
            },
            f,
        )


def main() -> None:
    data = get_data()
    plotter_main(data["google"][1]["chart_data"], data["reddit"]["chart_data"])

    if not os.path.exists(REDDIT_JSON_DIR):
        os.makedirs(REDDIT_JSON_DIR)

    if not os.path.exists(GOOGLE_JSON_DIR):
        os.makedirs(GOOGLE_JSON_DIR)
    save_reddit_data_as_json(data)
    save_google_data_as_json(data)


if __name__ == "__main__":
    main()
