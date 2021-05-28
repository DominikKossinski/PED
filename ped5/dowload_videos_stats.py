import json
import os
import traceback
from typing import Optional

import pandas as pd
import requests
from tqdm import tqdm

from helpers.files import load_csv, save_csv


def download_video_details(video_id: str, region_code: str) -> Optional[dict]:
    api_key = os.getenv("API_KEY")
    link = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&" \
           f"regionCode={region_code}&" \
           f"part=snippet%2Cstatistics&" \
           f"key={api_key}"
    try:
        response = requests.get(link)
        if response.status_code != 200:
            return None
        body = json.loads(response.content.decode("utf-8"))
        if len(body["items"]) < 1:
            return None

        item_body = body["items"][0]
        snippet = item_body["snippet"]
        statistics = item_body["statistics"]

        title = snippet.get("title", "")
        thumbnail = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        description = snippet.get("description", "")
        channel_title = snippet.get("channelTitle", "")
        category_id = snippet.get("categoryId", "")
        published_time = snippet.get("publishedAt", "")
        tags = "|".join(snippet.get("tags", []))
        views = statistics.get("viewCount", 0)

        if 'likeCount' in statistics and 'dislikeCount' in statistics:
            likes = statistics['likeCount']
            dislikes = statistics['dislikeCount']
            ratings_disabled = False
        else:
            ratings_disabled = True
            likes = 0
            dislikes = 0

        if 'commentCount' in statistics:
            comment_count = statistics['commentCount']
            comments_disabled = False
        else:
            comments_disabled = True
            comment_count = 0
        return {
            "video_id": video_id,
            "title": title,
            "channel_title": channel_title,
            "category_id": category_id,
            "publish_time": published_time,
            "tags": tags,
            "views": views,
            "likes": likes,
            "dislikes": dislikes,
            "comment_count": comment_count,
            "thumbnail_link": thumbnail,
            "comments_disabled": comments_disabled,
            "ratings_disabled": ratings_disabled,
            "video_error_or_removed": False,
            "description": description
        }
    except Exception as e:
        traceback.print_exc()
        print(f"Error by getting video ({video_id}): {e}")
        return None


def get_data(region_code: str):
    if region_code == "GB":
        data, _ = load_csv("ped5_data")
    elif region_code == "US":
        _, data = load_csv("ped5_data")
    else:
        raise ValueError(f"No country {region_code}")
    return data["video_id"]


def download_videos(region_code: str) -> None:
    data_ids = get_data(region_code)
    print(data_ids)

    mapped_items = {
        "video_id": [],
        "title": [],
        "channel_title": [],
        "category_id": [],
        "publish_time": [],
        "tags": [],
        "views": [],
        "likes": [],
        "dislikes": [],
        "comment_count": [],
        "thumbnail_link": [],
        "comments_disabled": [],
        "ratings_disabled": [],
        "video_error_or_removed": [],
        "description": []
    }
    for item_id in tqdm(data_ids):
        item = download_video_details(item_id, region_code)
        # print(item)
        if item is None:
            continue
        for key in item.keys():
            mapped_items[key].append(item[key])
    mapped_items = pd.DataFrame(data=mapped_items)
    save_csv("ped5_full_data", [mapped_items], [f"{region_code}_videos"])


def main():
    download_videos("GB")
    download_videos("US")


if __name__ == '__main__':
    main()
