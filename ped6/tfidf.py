import os
from typing import Tuple, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from helpers.json_helper import load_json_file


def add_tfidf_args(name: str, max_features: int) -> Tuple[pd.DataFrame, List]:
    tokenized_path = os.path.join(os.path.dirname(__file__), "..", "ped5_t_filtered", "tokenized")
    gb_trending_tokens = load_json_file(os.path.join(tokenized_path, f"GB_{name}.json"))
    us_trending_tokens = load_json_file(os.path.join(tokenized_path, f"US_{name}.json"))

    tokenized_path = os.path.join(os.path.dirname(__file__), "..", "ped5_nt_filtered", "tokenized")
    gb_non_trending_tokens = load_json_file(os.path.join(tokenized_path, f"GB_{name}.json"))
    us_non_trending_tokens = load_json_file(os.path.join(tokenized_path, f"US_{name}.json"))
    data = []
    for data_set in ([gb_trending_tokens, us_trending_tokens, gb_non_trending_tokens, us_non_trending_tokens]):
        for tokens_list in data_set:
            if tokens_list:
                data.append(" ".join(tokens_list))
            else:
                data.append("")
    vectorizer = TfidfVectorizer(max_features=max_features)
    tf_idf = vectorizer.fit_transform(data)
    tf_idf = pd.DataFrame.sparse.from_spmatrix(tf_idf)
    tf_idf = tf_idf.reset_index(drop=True)
    # print(f"All: {len(data)}")
    # print(f"Tfidf: {tf_idf.shape}")
    return tf_idf, vectorizer.get_feature_names()
