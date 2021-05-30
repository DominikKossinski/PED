import json
import math
import os

import pandas as pd
from tqdm import tqdm

from helpers.files import load_csv
from helpers.tokenizers import Tokenizer


def tokenize(csv_path: str, df: pd.DataFrame, attr_name: str, json_path: str):
    nan_count = 0
    if os.path.exists(csv_path):
        words = pd.read_csv(csv_path, sep=";")
        words = words["words"].to_frame()
        with open(json_path, "r") as file:
            tokenized_titles = json.load(file)
            file.close()
        for i in tqdm(tokenized_titles):
            if not i:
                nan_count += 1
    else:
        words = pd.DataFrame()
        tokenized_titles = []
        for i in tqdm(range(len(df)), desc=f"Tokenizing attr: {attr_name}"):
            text = df[attr_name].iloc[i]
            if isinstance(text, str):
                tokens = Tokenizer.tokenize(text)
                tokenized_titles.append(tokens)
                words = words.append(pd.DataFrame(data={"words": Tokenizer.tokenize(df[attr_name].iloc[i])}),
                                     ignore_index=True)
            elif isinstance(text, float):
                if math.isnan(text):
                    nan_count += 1
                    tokenized_titles.append([])
            else:
                print(text, type(text))
                tokenized_titles.append([])
        words.to_csv(csv_path, sep=";")
        with open(json_path, "w") as file:
            json.dump(tokenized_titles, file)
            file.close()
    print(len(tokenized_titles))
    print(f"Nan: {nan_count}")
    words_counts = words.value_counts()
    words_counts = words_counts.rename_axis("words").reset_index(name="count")
    print(words_counts)
    return words_counts


def main():
    gb_data, us_data = load_csv("ped5_full_data")

    dir_path = os.path.join(os.path.dirname(__file__), "..", "non_trending")
    os.makedirs(dir_path, exist_ok=True)

    json_path = os.path.join(dir_path, "tokenized")
    os.makedirs(json_path, exist_ok=True)
    words_path = os.path.join(dir_path, "words")
    os.makedirs(words_path, exist_ok=True)

    attrs = ["title", "channel_title", "description"]
    for attr in attrs:
        for df, code in zip([gb_data, us_data], ["GB", "US"]):
            json_file_path = os.path.join(json_path, f"{code}_{attr}.json")
            words_file_path = os.path.join(words_path, f"{code}_{attr}.csv")
            tokenize(words_file_path, df, attr, json_file_path)


if __name__ == '__main__':
    main()
