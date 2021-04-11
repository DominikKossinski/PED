import pandas as pd
import json
import os
import string
from helpers.tokenizers import Tokenizer
import matplotlib.pyplot as plt
from tqdm import tqdm
import math


def main():
    gb_videos = pd.read_csv(os.path.join("youtube_data_with_new_id", "GB_videos_5p.csv"), sep=";")
    us_videos = pd.read_csv(os.path.join("youtube_data_with_new_id", "US_videos_5p.csv"), sep=";")
    videos = pd.concat([gb_videos, us_videos])
    videos = videos.rename(columns={"description ": "description"})

    grouped_by_id = videos.groupby(["new_video_id"])
    print(grouped_by_id["trending_date"].nunique())

    exit(-123)
    videos = pd.concat([gb_videos, us_videos])
    videos = videos.rename(columns={"description ": "description"})
    description_counts = videos["description"].value_counts()
    description_counts = description_counts.rename_axis("description").reset_index(name="count")

    print(description_counts.describe())

    print(description_counts)
    plt.boxplot(description_counts["count"])
    plt.show()

    print(string.punctuation)
    # %%

    description_nan_count = 0

    words = pd.DataFrame()
    tokenized_descriptions_test = []
    for i in tqdm(range(len(videos))):
        text = videos["description"].iloc[i]
        if isinstance(text, str):
            tokens = Tokenizer.tokenize(text)
            tokenized_descriptions_test.append(tokens)
            words = words.append(pd.DataFrame(data={"words": Tokenizer.tokenize(videos["description"].iloc[i])}),
                                 ignore_index=True)
        elif isinstance(text, float):
            if math.isnan(text):
                description_nan_count += 1
                tokenized_descriptions_test.append([])
        else:
            print(text, type(text))
            tokenized_descriptions_test.append([])
        if i == 20_000:
            break
    words.to_csv("description_words_test.csv")
    with open("tokenized/tokenized_descriptions_test.json", "w") as file:
        json.dump(tokenized_descriptions_test, file)
        file.close()


    print(len(tokenized_descriptions_test))
    print(f"Nan: {description_nan_count}")
    print(words)
    words_counts = words.value_counts()
    words_counts = words_counts.rename_axis("words").reset_index(name="count")
    print(words_counts)
    wh = words_counts.head(50)
    plt.subplots(figsize=(18, 5))
    plt.bar(wh["words"], wh["count"])
    plt.title("50 najczęściej")
    plt.xticks(rotation=270, fontsize=15)
    plt.show()

    print(words_counts.head(50))
    w = words_counts["words"].iloc[15]
    for i in string.punctuation:
        w = w.replace(i, '')
    print(w)
    print(words_counts["words"].iloc[15])


if __name__ == '__main__':
    main()
