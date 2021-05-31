import json
import os
import re
from typing import List

import pandas as pd
from tqdm import tqdm

from helpers.files import load_csv, save_csv
from helpers.json_helper import load_json_file
from helpers.tokenizers import RE_HTTP


def extract_domains(tokenized_descriptions: List[List[str]], csv_path: str, json_path: str):
    domains = pd.DataFrame()
    all_domains_data = []
    domains_counts = pd.DataFrame()
    for tokens in tqdm(tokenized_descriptions):
        domains_list = []
        for token in tokens:
            if re.match(RE_HTTP, token):
                f = token.index("://")
                link = token[f + 3:]
                if "/" in link:
                    l = link.index("/")
                    domain = link[:l]
                else:
                    domain = link
                domain = domain.replace("www.", "")
                domains_list.append(domain)
        all_domains_data.append(domains_list)
        domains_counts = domains_counts.append(pd.DataFrame(data={"movie_domains_count": [len(domains_list)]}),
                                               ignore_index=True)
        domains = domains.append(pd.DataFrame(data={"domain": domains_list}), ignore_index=True)
    domains.to_csv(csv_path, sep=";")
    with open(json_path, "w") as file:
        json.dump(all_domains_data, file)
        file.close()
    return domains_counts


def main():
    dir_path = os.path.join(os.path.dirname(__file__), "..", "non_trending")
    os.makedirs(dir_path, exist_ok=True)

    json_path = os.path.join(dir_path, "tokenized")
    os.makedirs(json_path, exist_ok=True)
    words_path = os.path.join(dir_path, "words")
    os.makedirs(words_path, exist_ok=True)

    attr = "description"
    gb_data, us_data = load_csv("ped5_full_data")
    for data, code in zip([gb_data, us_data], ["GB", "US"]):
        tokenized_path = os.path.join(json_path, f"{code}_{attr}.json")
        tokenized_descriptions = load_json_file(tokenized_path)
        json_file_path = os.path.join(json_path, f"{code}_domain.json")
        csv_file_path = os.path.join(words_path, f"{code}_domain.csv")
        domains_counts = extract_domains(tokenized_descriptions, csv_file_path, json_file_path)
        print(len(data), len(domains_counts))
        data["movie_domains_count"] = domains_counts["movie_domains_count"]
    save_csv("ped5_full_data", [gb_data, us_data], ["GB_videos", "US_videos"])


if __name__ == '__main__':
    main()
