import numpy as np
import pandas as pd
from numpy import nan

from helpers.files import load_csv, save_csv

if __name__ == '__main__':
    nan
    numeric_attrs = [
        "views", "likes", "dislikes", "comment_count", "description_len", "title_len", "channel_title_len",
        "publish_time_day_of_week", "publish_time_hour_of_day", "publish_time", "movie_domains_count"
    ]

    bool_attrs = [
        "comments_disabled", "ratings_disabled", "video_error_or_removed"
    ]
    selecelected_attrs = ["new_video_id", "video_id", "title", "channel_title", "category_id", "publish_time", "tags",
                          "views", "likes", "dislikes", "comment_count", "thumbnail_link", "comments_disabled",
                          "ratings_disabled", "video_error_or_removed", "description", "description_len", "title_len",
                          "channel_title_len", "publish_time_day_of_week", "publish_time_hour_of_day",
                          "movie_domains_count"]

    gb_videos, us_videos = load_csv("ped3_data")
    trending_videos = pd.concat([gb_videos, us_videos])

    for name in numeric_attrs:
        trending_videos[name] = trending_videos[name].apply(lambda x: eval(x)[-1] if eval(x) else np.nan)
    trending_videos["tags"] = trending_videos["tags"].apply(lambda x: eval(x)[-1] if eval(x) else np.nan)

    for name in bool_attrs:
        trending_videos[name] = trending_videos[name].apply(lambda x: eval(x)[-1] if eval(x) else np.nan)
    trending_videos = trending_videos[selecelected_attrs]

    gb_videos = trending_videos.head(len(gb_videos))
    us_videos = trending_videos.tail(len(us_videos))
    save_csv("ped5_trending_original", [gb_videos, us_videos], ["GB_videos", "US_videos"])
