import lainista.reddit as reddit
import lainista.google_trends as google_trends
import json

reddit_data = reddit.main()
#google_trends_data = google_trends.main()

with open("./google_data.json", "w+") as f:
    f.write(json.dumps(reddit_data, indent=4, sort_keys=True))
