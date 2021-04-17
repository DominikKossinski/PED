import json
import os


def get_categories_dict() -> dict:
    path = os.path.dirname(__file__)
    path = os.path.join(path, "..", "youtube_data")
    file_names = list(filter(lambda name: ".json" in name, os.listdir(path)))
    categories_dict = dict()
    for name in file_names:
        with open(os.path.join(path, name), "r") as file:
            categories = json.load(file)
            file.close()
        for category in categories["items"]:
            if category["id"] in categories_dict:
                title = category["snippet"]["title"]
                if categories_dict[category["id"]] != title:
                    raise ValueError(category)
            else:
                title = category["snippet"]["title"]
                categories_dict[int(category["id"])] = str(title)
    return categories_dict
