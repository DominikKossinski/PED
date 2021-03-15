import pandas as pd
import os
from urllib import request
from tqdm import tqdm
import requests


def download(name: str):
    os.makedirs(name, exist_ok=True)
    gb_videos = pd.read_csv(os.path.join("youtube_data", "GB_videos_5p.csv"), sep=";")
    us_videos = pd.read_csv(os.path.join("youtube_data", "US_videos_5p.csv"), sep=";")
    videos = pd.concat([gb_videos, us_videos])
    videos = videos.rename(columns={"description ": "description"})
    videos_images = pd.DataFrame()
    for i in tqdm(range(len(videos))):
        link = videos["thumbnail_link"].iloc[i]
        id = videos["video_id"].iloc[i]
        link = link.replace("default", name)
        thumbnail_path = os.path.join(name, f"{i}.jpg")
        try:
            response = requests.get(link, allow_redirects=True)
            if response.status_code != 200:
                if response.status_code != 404:
                    print(response.status_code)
                    print("Error")
                thumbnail_path = thumbnail_path.replace(f"{i}.jpg", "error.jpg")
                videos_images = videos_images.append(
                    pd.DataFrame(
                        data={"number": [i], "id": [id], "thumbnail_path": [thumbnail_path], "error": [True],
                              "status": [response.status_code]})
                )
            else:
                videos_images = videos_images.append(
                    pd.DataFrame(
                        data={"number": [i], "id": [id], "thumbnail_path": [thumbnail_path], "error": [False],
                              "status": [response.status_code]})
                )
                with open(thumbnail_path, "wb") as file:
                    file.write(response.content)
                    file.flush()
                    file.close()
        except Exception as e:
            print(e)
    videos_images.to_csv(f"{name}.csv")


if __name__ == '__main__':
    download("hqdefault")
    # default - default size
    # hqdefault - bigger size
    # maxresdefault - max size
