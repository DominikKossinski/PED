import pandas as pd
from tqdm import tqdm

from helpers.files import load_csv, save_csv
from ped5.dowload_videos_stats import download_video_details


def get_data(region_code: str):
    if region_code == "GB":
        data, _ = load_csv("youtube_grouped_by_id")
    elif region_code == "US":
        _, data = load_csv("youtube_grouped_by_id")
    else:
        raise ValueError(f"No country {region_code}")
    return data["new_video_id"]


def download_videos(region_code: str) -> None:
    data_ids = get_data(region_code)
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
    save_csv("ped5_trending", [mapped_items], [f"{region_code}_videos"])


def main():
    download_videos("GB")
    download_videos("US")


if __name__ == '__main__':
    main()
