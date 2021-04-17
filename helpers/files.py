import os
from typing import List


def get_csv_files(dir_path: str) -> List[str]:
    if not os.path.isdir(dir_path):
        raise ValueError("Path is not directory")
    return list(filter(lambda x: x.endswith(".csv"), os.listdir(dir_path)))
