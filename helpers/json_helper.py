import json
import os
from typing import List


def load_tokenized_text(path: str) -> List[List[str]]:
    with open(path, "r") as file:
        tokenized = json.load(file)
        file.close()
    return tokenized


def save_grouped_tokenized(path: str, data: List[List[List[str]]]) -> None:
    with open(path, "w") as file:
        json.dump(data, file)
        file.close()


def save_frequent_tokens_dict(name: str, frequent_tokens: dict) -> None:
        path = os.path.dirname(__file__)
        path = os.path.join(path, "..", "frequent_tokens")
        os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, f"{name}.json"), "w") as file:
        json.dump(frequent_tokens, file)
        file.close()


def load_frequent_tokens_dict(name: str) -> dict:
    path = os.path.dirname(__file__)
    path = os.path.join(path, "..", "frequent_tokens")
    with open(os.path.join(path, f"{name}.json"), "r") as file:
        frequent_tokens = json.load(file)
        file.close()
    return frequent_tokens
