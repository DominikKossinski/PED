import os
import pandas as pd


def extract_id(video_id, link) -> str:
    new_id = link.replace("/default.jpg", "")
    i = new_id.rfind("/")
    new_id = new_id[i + 1:]
    if video_id == "#NAZWA?":
        print(video_id)
        print(link)
        print(new_id)
        return new_id
    if video_id != new_id:
        print("Error")
        print(video_id)
        print(new_id)
        print("\n")
    return video_id


def preprocess_ids(new_data_dir: str, file_name: str) -> None:
    videos = pd.read_csv(os.path.join("youtube_data", file_name), sep=";")
    videos["new_video_id"] = videos.apply(lambda x: extract_id(x["video_id"], x["thumbnail_link"]), axis=1)
    videos.to_csv(os.path.join(new_data_dir, file_name), sep=";")


def main():
    new_data_dir = "youtube_data_with_new_id"
    os.makedirs(new_data_dir, exist_ok=True)
    names = ["GB_videos_5p.csv", "US_videos_5p.csv"]
    for name in names:
        preprocess_ids(new_data_dir, name)


if __name__ == '__main__':
    main()
