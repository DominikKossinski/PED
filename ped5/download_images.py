import os

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm

from helpers.files import load_csv
from imgprocessing.image_size import ImageSize


def download_videos_images(videos: pd.DataFrame, prefix: str, size: ImageSize, path: str):
    videos_images = pd.DataFrame()
    whole_dir = os.path.join(path, size.value)
    for i in tqdm(range(len(videos)), desc=f"Downloading {prefix} {size}"):
        link = videos["thumbnail_link"].iloc[i]
        id = videos["video_id"].iloc[i]
        if size != ImageSize.default:
            link = link.replace("default", size.value)
        thumbnail_path = os.path.join(whole_dir, f"{i}_{prefix}_{id}.jpg")
        try:
            response = requests.get(link, allow_redirects=True)
            if response.status_code != 200:
                if response.status_code != 404:
                    print(response.status_code)
                    print("Error")
                thumbnail_path = "ERROR"
                error = True
                status = response.status_code
            else:
                error = False
                status = response.status_code
                with open(thumbnail_path, "wb") as file:
                    file.write(response.content)
                    file.flush()
                    file.close()
        except Exception as e:
            print(e)
            error = True
            status = np.nan
        videos_images = videos_images.append(
            pd.DataFrame(
                data={"number": [i], "id": [id], "thumbnail_path": [thumbnail_path], "error": [error],
                      "status": [status]})
        )
    videos_images.to_csv(os.path.join(path, f"{prefix}_{size}.csv"), sep=";")


def main():
    non_trending_path = os.path.join(os.path.dirname(__file__), "..", "non_trending")
    os.makedirs(non_trending_path, exist_ok=True)

    gb_data, us_data = load_csv("ped5_full_data")

    for size in list(ImageSize):
        size_dir = size.value
        whole_dir = os.path.join(non_trending_path, size_dir)
        os.makedirs(whole_dir, exist_ok=True)
        for df, code in zip([gb_data, us_data], ["GB", "US"]):
            download_videos_images(gb_data, code, size, non_trending_path)


if __name__ == '__main__':
    main()
