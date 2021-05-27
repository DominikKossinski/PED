# Base attrs:

# video_id - /search;
# trending_date - skipped -> generated by data set author;
# title - /search;
# description - /search
# thumbnail_link - /search thumbnails->default->url;
# publish_time - publishedAt /search;

# channel_title - /videos by id;
# category_id - /videos by id;
# tags - /videos by id;
# views - /videos by id;
# likes - /videos by id;
# dislikes - /videos by id;
# comment_count - /videos by id;
# comments_disabled - /videos by id;
# ratings_disabled  - /videos by id;
# video_error_or_removed - /videos by id;

import json
import os
import sys
import traceback
from argparse import ArgumentParser
from typing import List, Optional, Tuple

import pandas as pd
# Date format: 2017-12-25T20:21:57.000Z
# Min publishedAfter: 2017-11-01T00:00:00.000Z
# Max publishedAfter: 2018-06-30T00:00:00.000Z
import requests
from tqdm import tqdm

from helpers.files import load_csv, save_csv


# curl \
#   'https://youtube.googleapis.com/youtube/v3/search?
#       maxResults=50&
#       publishedAfter=2017-11-01T00%3A00%3A00Z&
#       publishedBefore=2018-06-30T00%3A00%3A00Z&
#       regionCode=GB&
#       type=video&
#       videoCategoryId=2&
#       key=[YOUR_API_KEY]' \
#   --header 'Accept: application/json' \
#   --compressed


def setup_args_parser() -> ArgumentParser:
    args_parser = ArgumentParser()
    args_parser.add_argument("--region-code", help="Region code (GB or US)", default="US")
    # args_parser.add_argument("--published_after", help="Format: yyyy-MM-ddTHH:mm:ssZ", type=str,
    #                          default="2017-11-01T00:00:00Z")
    # args_parser.add_argument("--published_before", help="Format: yyyy-MM-ddTHH:mm:ssZ", type=str,
    #                          default="2018-06-30T00:00:00Z")
    return args_parser


def get_time_intervals() -> List[Tuple[str, str]]:
    return [
        ("2017-11-01T00:00:00.000Z", "2018-01-01T00:00:00.000Z"),
        ("2018-01-01T00:00:00.000Z", "2018-03-01T00:00:00.000Z"),
        ("2018-03-01T00:00:00.000Z", "2018-05-01T00:00:00.000Z"),
        ("2018-05-01T00:00:00.000Z", "2018-07-01T00:00:00.000Z")
    ]


def get_categories_nums(categories_ids: List[str]) -> List[int]:
    nums_dict = {
        "24": 3,
        "10": 3,
        "26": 2,
        "22": 2,
        "23": 2,
        "17": 2,
        "25": 2,
        "1": 1,
        "28": 1,
        "27": 1,
        "20": 1,
        "15": 1,
        "2": 1,
        "19": 1,
        "29": 1
    }
    return [nums_dict[key] for key in categories_ids]


def get_category_ids(region_code: str):
    if region_code == "GB":
        videos, _ = load_csv("clustering_data")
    elif region_code == "US":
        _, videos = load_csv("clustering_data")
    else:
        raise ValueError(f"No country {region_code}")

    # inconsistency in data
    videos["category_id"] = videos["category_id"].replace(43.0, 24.0)
    category_ids = videos["new_category_id"].dropna().unique().tolist()
    # names_dict = get_categories_dict()
    # names = [names_dict[i] for i in category_ids]
    # return names
    return [str(int(x)) for x in category_ids]


def extract_video_details(item_body, category_id: str) -> Optional[dict]:
    snippet = item_body.get("snippet", None)
    video_id = item_body.get("id", dict()).get("videoId", "")
    if video_id == "" or snippet is None:
        return None
    title = snippet.get("title", "")
    thumbnail = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
    description = snippet.get("description", "")
    channel_title = snippet.get("channelTitle", "")
    published_time = snippet.get("publishedAt", "")

    return {
        "video_id": video_id,
        "title": title,
        "channel_title": channel_title,
        "category_id": category_id,
        "publish_time": published_time,
        # "tags": tags,
        # "views": views,
        # "likes": likes,
        # "dislikes": dislikes,
        # "comment_count": comment_count,
        "thumbnail_link": thumbnail,
        # "comments_disabled": comments_disabled,
        # "ratings_disabled": ratings_disabled,
        "video_error_or_removed": False,
        "description": description
    }


def get_trending_ids(region_code: str) -> List[str]:
    if region_code == "GB":
        data, _ = load_csv("youtube_grouped_by_id")
    elif region_code == "US":
        _, data = load_csv("youtube_grouped_by_id")
    else:
        raise ValueError(f"No country {region_code}")
    return data["new_video_id"].tolist()


def map_items_to_data(items, category_ids, excluded_ids, category_id, downloaded_ids) -> Tuple[pd.DataFrame, List[str]]:
    mapped_items = {
        "video_id": [],
        "title": [],
        "channel_title": [],
        "category_id": [],
        "publish_time": [],
        # "tags": [],
        # "views": [],
        # "likes": [],
        # "dislikes": [],
        # "comment_count": [],
        "thumbnail_link": [],
        # "comments_disabled": [],
        # "ratings_disabled": [],
        "video_error_or_removed": [],
        "description": []
    }
    not_video = 0
    excluded = 0
    not_category = 0
    none_count = 0
    downloaded_count = 0
    for item in tqdm(items, desc=f"Mapping category {category_id}"):
        kind = item.get("id", dict()).get("kind", "")
        if kind != "youtube#video":
            not_video += 1
            continue
        video_id = item.get("id", dict()).get("videoId", "")
        if video_id in excluded_ids or video_id == "":
            excluded += 1
            continue
        if video_id in downloaded_ids:
            downloaded_count += 1
            continue
        else:
            item_data = extract_video_details(item, category_id)
            if item_data is None:
                none_count += 1
                continue
            if str(item_data["category_id"]) not in category_ids:
                not_category += 1
                continue
            if item_data is not None:
                downloaded_ids.append(video_id)
                for key in item_data.keys():
                    mapped_items[key].append(item_data[key])
    print(f"Excluded ids count: {excluded}")
    print(f"Excluded categories count: {not_category}")
    print(f"Not video count: {not_video}")
    print(f"None count: {none_count}")
    print(f"Already downloaded: {downloaded_count}")
    data = pd.DataFrame(data=mapped_items)
    print(f"MappedLen: {len(data)}")
    return data, downloaded_ids


def main(args):
    category_ids = get_category_ids(args["region_code"])
    nums = get_categories_nums(category_ids)
    print(nums)
    print(f"Sum: {sum(nums) * len(get_time_intervals())}")
    download_data(args["region_code"], category_ids, nums)


def download_data(region_code: str, category_ids: list, nums: list) -> None:
    path = os.path.dirname(__file__)
    path = os.path.join(path, "..", "ped5_data")
    # Create csv dir
    os.makedirs(path, exist_ok=True)

    excluded_ids = get_trending_ids(region_code)
    api_key = os.getenv("API_KEY")
    total_count = 0
    videos = pd.DataFrame()
    downloaded_ids = []
    requests_count = 0
    for published_after, published_before in get_time_intervals():
        for category_id, num in zip(category_ids, nums):
            i = 0
            next_page_token = ""
            while i < num and next_page_token is not None:
                i += 1
                try:
                    link = f"https://www.googleapis.com/youtube/v3/search?" \
                           f"chart=mostPopular&" \
                           f"regionCode={region_code}&" \
                           f"{next_page_token}" \
                           f"type=video&" \
                           f"videoCategoryId={category_id}&" \
                           f"publishedAfter={published_after}&" \
                           f"publishedBefore={published_before}&" \
                           f"maxResults=50&" \
                           f"part=snippet&" \
                           f"key={api_key}"
                    print(link)

                    response = requests.get(link) # TODO uncomment
                    requests_count += 1
                    # print(response)
                    body = get_mock_body() # TODO comment
                    body = response.content.decode("utf-8") # TODO uncomment
                    body = json.loads(body) # TODO uncomment
                    if response.status_code == 200: # TODO uncomment
                        print(body)
                        page_info = body.get("pageInfo", dict())
                        print(f"TotalResults: {page_info.get('totalResults', None)}")
                        items = body.get("items", [])
                        data, downloaded_ids = map_items_to_data(items, category_ids, excluded_ids, category_id,
                                                                 downloaded_ids)
                        videos = pd.concat([videos, data], ignore_index=True)
                        page_token = body.get("nextPageToken", None)
                        if page_token is None:
                            next_page_token = None
                        else:
                            next_page_token = f"pageToken={body['nextPageToken']}&"
                        total_count += len(data)
                        print(f"Total count: {total_count}")
                    else:
                        print(body, file=sys.stderr)
                        next_page_token = None

                except Exception as e:
                    traceback.print_exc()
                    print(f"Error: {e}")
    save_csv("ped5_data", [videos], [f"{region_code}_videos"])
    save_csv("ped5_requests", [pd.DataFrame(data={"request_count": [requests_count]})], [f"{region_code}_requests"])


def get_mock_body():
    with open("mock_body.json", "r") as file:
        lines = "\n".join(file.readlines())
        file.close()
    return json.loads(lines)


if __name__ == '__main__':
    parser = setup_args_parser()
    main(vars(parser.parse_args()))
