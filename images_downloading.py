import os
from argparse import ArgumentParser
from enum import Enum

import requests
from tqdm import tqdm

import pandas as pd


class ImageSize(Enum):
    default = "default"
    hqdefault = "hqdefault"
    maxresdefault = "maxresdefault"

    def __str__(self):
        return self.value


def setup_args_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--size", help="Image size", type=ImageSize, choices=list(ImageSize),
                            default=ImageSize.default.value)
    return arg_parser


def download_videos_images(videos: pd.DataFrame, prefix: str, size: ImageSize, path: str):
    videos_images = pd.DataFrame()
    whole_dir = os.path.join(path, size.value)
    for i in tqdm(range(len(videos)), desc=f"Downloading {prefix[:-1]}"):
        links = videos["thumbnail_link"].iloc[i]
        if not isinstance(links, list):
            links = [links]
        paths = []
        statuses = []
        errors = []
        for j, link in enumerate(links):
            id = videos["new_video_id"].iloc[i]
            count = videos["count"].iloc[i]
            if size != ImageSize.default:
                link = link.replace("default", size.value)
            thumbnail_path = os.path.join(whole_dir, f"{i}_{prefix}{id}_{j}.jpg")
            try:
                response = requests.get(link, allow_redirects=True)
                if response.status_code != 200:
                    if response.status_code != 404:
                        print(response.status_code)
                        print("Error")
                    thumbnail_path = "ERROR"
                    paths.append(thumbnail_path)
                    errors.append(True)
                    statuses.append(response.status_code)
                else:
                    paths.append(thumbnail_path)
                    errors.append(False)
                    statuses.append(response.status_code)
                    with open(thumbnail_path, "wb") as file:
                        file.write(response.content)
                        file.flush()
                        file.close()
            except Exception as e:
                print(e)
            videos_images = videos_images.append(
                pd.DataFrame(
                    data={"number": [i], "id": [id], "count": [count], "thumbnail_path": [paths], "error": [errors],
                          "status": [statuses]})
            )

    videos_images.to_csv(os.path.join(path, f"{prefix}{size}.csv"))
    videos_images.to_pickle(os.path.join(path, f"{prefix}{size}.plk"))


def main(args):
    images_dir = "images"
    size_dir = args.size.value
    whole_dir = os.path.join(images_dir, size_dir)
    os.makedirs(whole_dir, exist_ok=True)
    data_dir = "youtube_grouped_by_id"
    names = os.listdir(data_dir)
    names = filter(lambda x: ".plk" in x, names)
    for name in names:
        print(name)
        prefix = name[:name.index("_") + 1]
        videos = pd.read_pickle(os.path.join(data_dir, name))
        download_videos_images(videos, prefix, args.size, images_dir)


if __name__ == '__main__':
    parser = setup_args_parser()
    main(parser.parse_args())
