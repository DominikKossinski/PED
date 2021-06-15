import json
import os

import numpy as np
import pandas as pd

from helpers.files import load_csv, save_csv


def load_tokens(json_path: str):
    with open(json_path, "r") as file:
        tokenized = json.load(file)
        file.close()
    return tokenized


def save_tokens_list(json_path, tokens):
    with open(json_path, "w") as file:
        json.dump(tokens, file)
        file.close()


def filter_dir(tokens_path, save_path, data, attrs, forbidden_tokens, codes=None):
    if codes is None:
        codes = ["GB", "US"]
    tokens_path = os.path.join(os.path.dirname(__file__), "..", tokens_path)
    save_tokens_path = os.path.join(os.path.dirname(__file__), "..", save_path)

    json_path = os.path.join(tokens_path, "tokenized")
    save_path = os.path.join(save_tokens_path, "tokenized")
    save_words_path = os.path.join(save_tokens_path, "words")
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(save_words_path, exist_ok=True)

    masks = [np.array([False] * len(df)) for df in data]
    for attr, forbidden in zip(attrs, forbidden_tokens):
        if len(forbidden) == 0:
            continue
        for mask, code, df in zip(masks, ["GB", "US"], data):
            json_file_path = os.path.join(json_path, f"{code}_{attr}.json")
            tokens_list = load_tokens(json_file_path)
            for i, tokens in enumerate(tokens_list):
                # if attr == "title":
                #     text = df.loc[i][attr]
                #     # print(type(text))
                #     # print(text)
                #     # exit(-123)
                #     try:
                #         langs = detect_langs(text)
                #         max_prob = 0
                #         lang = None
                #         for l in langs:
                #             if l.prob > max_prob:
                #                 max_prob = l.prob
                #                 lang = l.lang
                #         if max_prob > 0.3 and lang != "en":
                #             mask[i] = mask[i] or True
                #             print(langs)
                #             print(text)
                #             print(lang)
                #     except LangDetectException:
                #         print(f"Text: '{text}'")
                found = False
                for f in forbidden:
                    if f in tokens:
                        found = True
                        break
                mask[i] = mask[i] or found

    for i in range(len(masks)):
        masks[i] = np.invert(masks[i])

    for attr in attrs:
        print(attr)
        for mask, code in zip(masks, codes):
            json_file_path = os.path.join(json_path, f"{code}_{attr}.json")
            save_file_path = os.path.join(save_path, f"{code}_{attr}.json")
            save_words_file = os.path.join(save_words_path, f"{code}_{attr}.csv")
            tokens_list = load_tokens(json_file_path)
            print(len(tokens_list), len(mask))
            words = []
            new_tokens_list = []
            for i in range(len(mask)):
                if mask[i]:
                    words += tokens_list[i]
                    new_tokens_list.append(tokens_list[i])
            words_df = pd.DataFrame(data={"words": words})
            words_df.to_csv(save_words_file, sep=";")
            print(np.sum(mask), len(new_tokens_list))
            save_tokens_list(save_file_path, new_tokens_list)
    new_data = []
    for df, mask in zip(data, masks):
        new_data.append(df[mask == True].reset_index(drop=True))
    return new_data


def main():
    attrs = ["channel_title", "description", "domain", "tags", "title"]
    forbidden_tokens = [["jimmi", "bbc", "la", "de"], ["la", "de"], ["la", "de"],
                        ["la", "de"],
                        ["show", "vevo", "trailer", "comedi", "offici", "ft"]]

    gb_non_videos, us_non_videos = load_csv("ped5_non_trending")
    gb_non_filtered, us_non_filtered = filter_dir(
        "non_trending", "ped5_nt_filtered", [gb_non_videos, us_non_videos], attrs, forbidden_tokens
    )
    save_csv("ped5_nt_filtered", [gb_non_filtered, us_non_filtered], ["GB_videos", "US_videos"])

    gb_t_videos, us_t_videos = load_csv("ped5_trending_original")

    gb_t_filtered, us_t_filtered = filter_dir(
        "ped5_trending_original", "ped5_t_filtered", [gb_t_videos, us_t_videos], attrs, forbidden_tokens
    )
    save_csv("ped5_t_filtered", [gb_t_filtered, us_t_filtered], ["GB_videos", "US_videos"])


if __name__ == '__main__':
    main()
