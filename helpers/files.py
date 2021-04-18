import os
from typing import List

import pandas as pd


def get_csv_files(dir_path: str) -> List[str]:
    if not os.path.isdir(dir_path):
        raise ValueError("Path is not directory")
    return list(filter(lambda x: x.endswith(".csv"), os.listdir(dir_path)))


def save_csv(dir_name: str, frames: List[pd.DataFrame], names: List[str]) -> None:
    if len(frames) != len(names):
        ValueError("Number of frames not equal number of names")
    path = os.path.dirname(__file__)
    path = os.path.join(path, "..", dir_name)
    os.makedirs(path, exist_ok=True)
    for df, name in zip(frames, names):
        df.to_csv(os.path.join(path, f"{name}.csv"), sep=";")
