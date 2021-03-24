import os
import pandas as pd


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
    grouped = grouped.agg(lambda x: aggregate_to_list_or_value(x))

    # for column in grouped.columns:
    #     a = grouped[column].apply(lambda x: len(x) == 1)
    #     if a.all():
    #         print(column)
    #         grouped[column] = grouped[column].apply(lambda x: x[0])
    return grouped


def main():
    data_path = "youtube_data_with_new_id"
    grouped_data_path = "youtube_grouped_by_id_all_list"
    os.makedirs(grouped_data_path, exist_ok=True)
    names = os.listdir(data_path)
    for name in names:
        videos = pd.read_csv(os.path.join(data_path, name), sep=";", index_col=0)
        grouped_videos = group_by_id(videos).reset_index()
        grouped_videos.to_csv(os.path.join(grouped_data_path, name), sep=";")
        grouped_videos.to_pickle(os.path.join(grouped_data_path, name.replace(".csv", ".plk")))


if __name__ == '__main__':
    main()
