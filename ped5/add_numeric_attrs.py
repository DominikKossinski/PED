import pandas as pd

from helpers.files import load_csv, save_csv


def add_len_attrs(data: pd.DataFrame) -> pd.DataFrame:
    names = [("description_len", "description"), ("title_len", "title"), ("channel_title_len", "channel_title")]
    for name, attr in names:
        data[name] = data[attr].apply(lambda x: int(len(x)) if isinstance(x, str) else 0)
    print(data)
    return data


def add_time_attrs(data: pd.DataFrame) -> pd.DataFrame:
    data["publish_time_day_of_week"] = pd.to_datetime(data["publish_time"], format="%Y-%m-%dT%H:%M:%SZ").dt.dayofweek
    data["publish_time_hour_of_day"] = pd.to_datetime(data["publish_time"], format="%Y-%m-%dT%H:%M:%SZ").dt.hour
    return data


def process_dir(dir_name: str, save_dir: str):
    gb_data, us_data = load_csv(dir_name)
    gb_data = add_len_attrs(gb_data)
    us_data = add_len_attrs(us_data)
    gb_data = add_time_attrs(gb_data)
    us_data = add_time_attrs(us_data)
    save_csv(save_dir, [gb_data, us_data], ["GB_videos", "US_videos"])


def main():
    process_dir("ped5_non_trending", "ped5_non_trending")
    process_dir("ped5_trending", "ped5_trending")


if __name__ == '__main__':
    main()
