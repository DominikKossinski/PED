from argparse import ArgumentParser

import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import recall_score, accuracy_score, f1_score, precision_score, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.semi_supervised import LabelSpreading

from helpers.categories import get_categories_dict
from helpers.files import load_csv
from helpers.json_helper import load_tokenized_text


def setup_args_parser() -> ArgumentParser:
    parser = ArgumentParser()

    return parser


def get_mapping_dict(y_hat_nans, y_pred) -> dict:
    values_counts = y_hat_nans.value_counts().reset_index(name="count")
    # print(values_counts)
    # print(f"Index: {values_counts.index}")
    most_frequent_class = values_counts["index"].iloc[0]
    # print(most_frequent_class)
    mapping_dict = {}
    y_data = pd.DataFrame()
    y_data["y_hat_nans"] = y_hat_nans
    y_data["y"] = y_pred
    y_data["c"] = 1
    y_data = y_data.groupby(["y", "y_hat_nans"])["c"].sum()  # .max(level=[0])#.sort_values().groupby(level=0)
    # print(y_data)
    out = y_data.loc[y_data.groupby(level=0).idxmax()]
    # print(out)
    for row in out.index:
        mapping_dict[row[0]] = row[1]
    for i in range(np.unique(y_pred).shape[0]):
        if i not in mapping_dict.keys():
            mapping_dict[i] = most_frequent_class
    return mapping_dict


def show_stats(y_hat, y_hat_nans, y, mapped: bool = False):
    if not mapped:
        mapping_dict = get_mapping_dict(y_hat_nans, y)
        print(mapping_dict)
        y_mapped = pd.Series(y).apply(lambda x: mapping_dict[x])
    else:
        y_mapped = pd.Series(y.astype(np.int))
        y_hat = y_hat.astype(np.int)
    print(f"Accuracy: {accuracy_score(y_hat, y_mapped)}")
    print(f"F1: {f1_score(y_hat, y_mapped, average='macro')}")
    print(f"Precision: {precision_score(y_hat, y_mapped, average='macro')}")
    print(f"Recall: {recall_score(y_hat, y_mapped, average='macro')}")
    print(f"Hat unique:{np.unique(y_hat.to_numpy())}")
    print(f"labeled unique: {np.unique(y_mapped.to_numpy())}")
    print(f"y_hat_nans : {np.unique(y_hat_nans[y_hat_nans.notna()].to_numpy())}")
    y_hat = y_hat.to_numpy().reshape(-1, 1)
    y_mapped = y_mapped.to_numpy().reshape(-1, 1)
    encoder = OneHotEncoder(sparse=False)
    one_hot_hat = encoder.fit_transform(y_hat)
    y_hot = encoder.transform(y_mapped)
    print(f"ROC AUC Score OVR: {roc_auc_score(one_hot_hat, y_hot, multi_class='ovr')}")
    print(f"ROC AUC Score OVO: {roc_auc_score(one_hot_hat, y_hot, multi_class='ovo')}")


def add_tfidf_args(name: str) -> pd.DataFrame:
    gb_tokens = load_tokenized_text(f"GB_grouped_{name}")
    us_tokens = load_tokenized_text(f"US_grouped_{name}")
    gb_last_tokens = []
    us_last_tokens = []
    for data, l in zip([gb_tokens, us_tokens], [gb_last_tokens, us_last_tokens]):
        for tokens_list in data:
            if tokens_list:
                l.append(" ".join(tokens_list[0]))
            else:
                l.append("")
    data = gb_last_tokens + us_last_tokens

    vectorizer = TfidfVectorizer(max_features=200)
    tf_idf = vectorizer.fit_transform(data)
    tf_idf = pd.DataFrame.sparse.from_spmatrix(tf_idf)
    tf_idf = tf_idf.reset_index(drop=True)
    print(f"All: {len(data)}")
    print(f"Tfidf: {tf_idf.shape}")
    return tf_idf

def load_videos_with_tf_idf():
    gb_data, us_data = load_csv("clustering_data")
    videos = pd.concat([gb_data, us_data])
    # TODO check categories -> missing 43 add to note book
    videos["category_id"] = videos["category_id"].replace(43.0, 24.0)


    videos = videos.reset_index(drop=True)

    tf_idf_list = []
    names = ["channel_titles", "descriptions", "titles"]
    for name in names:
        df = add_tfidf_args(name)[videos["new_category_id"].notna()].reset_index(drop=True)
        tf_idf_list.append(df)

    videos = videos[videos["new_category_id"].notna()]
    videos = videos.reset_index(drop=True)

    categories_ids = videos["new_category_id"].dropna().unique().tolist()
    categories_dict = get_categories_dict()

    videos["tags"] = videos["tags"].apply(lambda x: " ".join(eval(x)[0].split("|")) if eval(x) else "")
    vectorizer = TfidfVectorizer(max_features=200)
    x_tags = vectorizer.fit_transform(videos["tags"])

    selected_columns = [
        "views", "likes", "dislikes", "comment_count", "description_len", "title_len", "channel_title_len",
        "publish_time_day_of_week", "publish_time_hour_of_day",
        "gray_mean_score", "color_mean_score", "gray_hist_score",
        "red_hist_score", "green_hist_score", "blue_hist_score", "edges_score", "entropy_score",
    ]

    for cat in categories_ids:
        selected_columns.append(f"freq_channel_titles_{categories_dict[cat]}")
        selected_columns.append(f"freq_titles_{categories_dict[cat]}")
        selected_columns.append(f"freq_tags_{categories_dict[cat]}")
        selected_columns.append(f"freq_descriptions_{categories_dict[cat]}")

    y_hat = videos["new_category_id"]  # oczekiwane kategorie z api
    y_hat_nans = videos["category_id"]  # oczekiwane kategorie z nanami (z oryginalnego zbioru)

    videos = videos[selected_columns]
    x_tags = pd.DataFrame.sparse.from_spmatrix(x_tags)
    videos = pd.concat([videos, x_tags], axis=1)
    for n, i in zip(names, tf_idf_list):
        print(i.shape)
        videos = pd.concat([videos, i], axis=1)

    videos = videos.replace([np.inf, -np.inf], np.nan)
    videos = videos.fillna(videos.mean())

    scaler = MinMaxScaler()
    videos = scaler.fit_transform(videos)

    videos = np.nan_to_num(videos)

    return videos
    # x_not_nan = videos[y_hat_nans.notna()]
    # y_not_nan = y_hat_nans[y_hat_nans.notna()]


def main(args) -> None:
    gb_data, us_data = load_csv("clustering_data")
    videos = pd.concat([gb_data, us_data])
    # TODO check categories -> missing 43 add to note book
    videos["category_id"] = videos["category_id"].replace(43.0, 24.0)
    print(f"Videos: {videos.shape}")

    print(videos[videos["category_id"] == 29.0])
    exit(-15)

    videos = videos.reset_index(drop=True)

    tf_idf_list = []
    names = ["channel_titles", "descriptions", "titles"]
    for name in names:
        df = add_tfidf_args(name)[videos["new_category_id"].notna()].reset_index(drop=True)
        tf_idf_list.append(df)

    videos = videos[videos["new_category_id"].notna()]
    videos = videos.reset_index(drop=True)

    print(f"New videos: {videos.shape}")

    categories_ids = videos["new_category_id"].dropna().unique().tolist()
    categories_dict = get_categories_dict()
    categories = [categories_dict[cat] for cat in categories_ids]

    videos["tags"] = videos["tags"].apply(lambda x: " ".join(eval(x)[0].split("|")) if eval(x) else "")
    vectorizer = TfidfVectorizer(max_features=200)
    x_tags = vectorizer.fit_transform(videos["tags"])

    selected_columns = [
        "views", "likes", "dislikes", "comment_count", "description_len", "title_len", "channel_title_len",
        "publish_time_day_of_week", "publish_time_hour_of_day",
        "gray_mean_score", "color_mean_score", "gray_hist_score",
        "red_hist_score", "green_hist_score", "blue_hist_score", "edges_score", "entropy_score",
    ]

    for cat in categories_ids:
        selected_columns.append(f"freq_channel_titles_{categories_dict[cat]}")
        selected_columns.append(f"freq_titles_{categories_dict[cat]}")
        selected_columns.append(f"freq_tags_{categories_dict[cat]}")
        selected_columns.append(f"freq_descriptions_{categories_dict[cat]}")

    y_hat = videos["new_category_id"]  # oczekiwane kategorie z api
    y_hat_nans = videos["category_id"]  # oczekiwane kategorie z nanami (z oryginalnego zbioru)

    videos = videos[selected_columns]
    x_tags = pd.DataFrame.sparse.from_spmatrix(x_tags)
    print(f"Videos: {videos.shape}")
    print(f"X tags: {x_tags.shape}")
    print(f"Tags shape : {x_tags.shape}")
    videos = pd.concat([videos, x_tags], axis=1)
    print(videos.shape)
    for n, i in zip(names, tf_idf_list):
        print(i.shape)
        videos = pd.concat([videos, i], axis=1)

    videos = videos.replace([np.inf, -np.inf], np.nan)
    videos = videos.fillna(videos.mean())

    scaler = MinMaxScaler()
    videos = scaler.fit_transform(videos)

    videos = np.nan_to_num(videos)

    x_not_nan = videos[y_hat_nans.notna()]
    y_not_nan = y_hat_nans[y_hat_nans.notna()]

    select = SelectKBest(chi2, k=100)
    x_not_nan = select.fit_transform(x_not_nan, y_not_nan)
    x = select.transform(videos)
    print(x_not_nan.shape)

    init_data = []
    for i in categories_ids:
        init_data.append(x_not_nan[y_not_nan == i][0])
        # print(x_not_nan[y_not_nan == i][0])
    init_data = np.array(init_data)
    print(f"Init shape: {init_data.shape}")

    # k_list = np.arange(2, 20)
    # inertias = np.zeros_like(k_list, dtype=np.float)
    # silhouettes = np.zeros_like(k_list, dtype=np.float)
    #
    # for i, k in enumerate(k_list):
    #     model = KMeans(k)
    #     # model.fit(x)
    #     labels = model.fit_predict(x)
    #     inertias[i] = model.inertia_
    #     silhouettes[i] = silhouette_score(x, labels)
    #
    # plt.plot(k_list, inertias)
    # plt.title("Interias")
    # plt.show()
    # plt.plot(k_list, silhouettes)
    # plt.title("Silhouette")
    # plt.show()

    model = KMeans(len(categories), init=init_data)
    model.fit(x)
    y = model.predict(x)
    show_stats(y_hat, y_hat_nans, y)
    print(x.shape)

    print("\n\nDBSCAN")
    model = DBSCAN(eps=0.2, min_samples=20)
    model.fit(x)
    y = model.labels_
    show_stats(y_hat, y_hat_nans, y)

    nn = NearestNeighbors(n_neighbors=11)
    neighbors = nn.fit(x)
    dist, ind = neighbors.kneighbors()

    dist = np.sort(dist[:, 10], axis=0)

    plt.plot(dist)
    plt.xlabel("Points")
    plt.ylabel("Dist")
    plt.show()

    parameters = {'kernel': ["knn", "rbf"], 'gamma': [1, 10, 20, 30, 40], 'n_neighbors': [3, 5, 7, 11]}

    best_auc = 0
    best_params = None
    scores = []

    params = []
    for k in parameters['kernel']:
        for g in parameters['gamma']:
            for n in parameters['n_neighbors']:
                params.append((k, g, n))
    for p in tqdm(params):
        k, g, n = p
        model = LabelSpreading(kernel=k, gamma=g, n_neighbors=7)
        model.fit(x_not_nan, y_not_nan)
        y = model.predict(x)
        y_mapped = y.reshape(-1, 1)
        encoder = OneHotEncoder(sparse=False)
        one_hot_hat = encoder.fit_transform(y_hat.to_numpy().reshape(-1, 1))
        y_hot = encoder.transform(y_mapped)
        score = roc_auc_score(one_hot_hat, y_hot, multi_class='ovr')
        scores.append((score, p))
        if score > best_auc:
            best_auc = score
            best_params = p

    print(f"Best params: {best_params}")
    print(f"BestScore: {best_auc}")
    print(f"Scores: {scores}")
    k, g, n = best_params
    model = LabelSpreading(kernel=k, gamma=g, n_neighbors=7)
    print("\n\nLabelSpreading")
    model.fit(x_not_nan, y_not_nan)
    print(f"classes: {model.classes_}")
    y = model.predict(x)
    show_stats(y_hat, y_hat_nans, y, True)

    # print("\n\nLabelPropagation")
    # model = LabelPropagation()
    # model.fit(x_not_nan, y_not_nan)
    # print(f"classes: {model.classes_}")
    # y = model.predict(x)
    # show_stats(y_hat, y_hat_nans, y, True)


if __name__ == '__main__':
    arg_parser = setup_args_parser()
    main(arg_parser.parse_args())
