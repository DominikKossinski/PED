import json
from typing import List


def load_tokenized_text(path: str) -> List[List[str]]:
    with open(path, "r") as file:
        tokenized = json.load(file)
        file.close()
    return tokenized


def save_grouped_tokenized(path: str, data: List[List[List[str]]]):
    with open(path, "w") as file:
        json.dump(data, file)
        file.close()
