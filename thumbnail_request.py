import pandas as pd
import os
from urllib import request
from tqdm import tqdm
import requests


def my_bar(current, total, width):
    print(f"Downloading {round(current / total * 100)}% ({current}/{total}) bytes: (", end="\r", flush=True)


if __name__ == '__main__':
    gb_videos = pd.read_csv(os.path.join("youtube_data", "GB_videos_5p.csv"), sep=";")
    us_videos = pd.read_csv(os.path.join("youtube_data", "US_videos_5p.csv"), sep=";")
    videos = pd.concat([gb_videos, us_videos])
    videos = videos.rename(columns={"description ": "description"})
    videos_images = pd.DataFrame()
    for i in tqdm(range(len(videos))):
        link = videos["thumbnail_link"].iloc[i]
        id = videos["video_id"].iloc[i]
        thumbnail_path = os.path.join("thumbnails", f"{i}.jpg")
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
    videos_images.to_csv("thumbnails.csv")
    # hqdefault - TODO bigger
    # maxresdefault - TODO max size
