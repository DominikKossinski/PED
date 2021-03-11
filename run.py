import pandas as pd
import json
import os
from categories import get_categories_dict

def main():
    get_categories_dict()
    exit(-4561)
    gb_videos = pd.read_csv(os.path.join("youtube_data", "GB_videos_5p.csv"), sep=";")
    print(gb_videos.head(20))
    print(gb_videos.shape)
    print(gb_videos.columns)
    print(gb_videos.dtypes)
    with open(os.path.join("youtube_data", "GB_category_id.json"), "r") as file:
        gb_category = json.load(file)
        file.close()
    print(len(gb_category["items"]))


if __name__ == '__main__':
    main()
