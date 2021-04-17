import os
import pandas as pd

from argparse import ArgumentParser

from helpers.files import get_csv_files
from helpers.json_helper import load_tokenized_text, save_grouped_tokenized


def setup_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()

    return arg_parser


def aggregate_to_list_or_value(x):
    l = list(x)
    s = set(l)
    if len(s) != len(l):
        return list(s)
    else:
        return l


def group_by_id(videos: pd.DataFrame):
    grouped = videos.groupby('new_video_id')
    videos["count"] = grouped["video_id"].transform("count")

    grouped = videos.groupby('new_video_id')
    print(f"v: {videos.columns}")
    grouped = grouped.agg(lambda x: aggregate_to_list_or_value(x))
    return grouped


def main(args) -> None:
    data_path = os.path.join("..", "youtube_data_with_new_id")
    tokenized_names = ["titles", "descriptions", "channel_titles"]
    names = get_csv_files(data_path)
    videos_list = []
    for name in names:
        videos_list.append(pd.read_csv(os.path.join(data_path, name), sep=";", index_col=0))
    tokenized_list = []
    for name in tokenized_names:
        tokenized = load_tokenized_text(os.path.join("..", "tokenized", f"tokenized_{name}.json"))
        print(f"{name}: {len(tokenized)}")
        tokenized_list.append(tokenized)

    for videos in videos_list:
        for i, name in enumerate(tokenized_names):
            videos[f"tokenized_{name}"] = tokenized_list[i][:len(videos)]
            videos[f"tokenized_{name}"] = videos[f"tokenized_{name}"].apply(lambda x: str(x))
            tokenized_list[i] = tokenized_list[i][len(videos):]
    countries = ["GB", "US"]
    for c, videos in zip(countries, videos_list):
        grouped_videos = group_by_id(videos)
        print(f"{c} : {len(grouped_videos)}")

        print(grouped_videos.columns)
        print(grouped_videos["tokenized_titles"])
        print(len(grouped_videos))
        for name in tokenized_names:
            grouped_videos[f"tokenized_{name}"] = grouped_videos[f"tokenized_{name}"].apply(
                lambda x: [eval(i) for i in x])
            print(len(grouped_videos[f"tokenized_{name}"]))
            save_grouped_tokenized(
                os.path.join("..", "tokenized", f"{c}_grouped_{name}.json"),
                grouped_videos[f"tokenized_{name}"].tolist()
            )


if __name__ == '__main__':
    parser = setup_arg_parser()
    main(parser.parse_args())
