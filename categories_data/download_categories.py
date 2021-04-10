import json
import os
import requests

import pandas as pd
import numpy as np

from tqdm import tqdm
from argparse import ArgumentParser


def setup_args_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--grouped-path", help="Path to grouped data set", type=str, required=True)
    arg_parser.add_argument("--path", help="Path to save directory", type=str, default="data")
    return arg_parser


def download_videos_categories(videos: pd.DataFrame, prefix: str, api_key: str) -> pd.DataFrame:
    categories = []
    for i in tqdm(range(len(videos)), desc=f"Downloading categories: {prefix[:-2]}"):
        id = videos["new_video_id"].iloc[i]
        link = f"https://www.googleapis.com/youtube/v3/videos?id={id}&part=snippet&key={api_key}"
        try:
            response = requests.get(link)
            if response.status_code != 200:
                if response.status_code != 404:
                    print(f"Error code {response.status_code}")
                categories.append(np.nan)
            else:
                string_resp = response.content.decode("utf-8")
                data = json.loads(string_resp)
                if len(data['items']) == 0:
                    categories.append(np.nan)
                elif len(data['items']) != 1:
                    print(data)
                    category_id = data['items'][0]['snippet']['categoryId']
                    categories.append(category_id)
                else:
                    category_id = data['items'][0]['snippet']['categoryId']
                    categories.append(category_id)
        except Exception as e:
            print(e)
    videos["new_category_id"] = categories
    return videos


def main(args):
    api_key = os.getenv("API_KEY")
    if args.path:
        os.makedirs(args.path, exist_ok=True)
    file_names = list(filter(lambda x: x.endswith(".csv"), os.listdir(args.grouped_path)))
    print(file_names)
    for name in file_names:
        prefix = name[:name.index("_") + 1]
        data = pd.read_csv(os.path.join(args.grouped_path, name), sep=";", index_col=0)
        categories_data = download_videos_categories(data, prefix, api_key)
        categories_data.to_csv(os.path.join(args.path, name), sep=";")


if __name__ == '__main__':
    parser = setup_args_parser()
    main(parser.parse_args())
