import os
import pandas as pd
from tqdm import tqdm

from imgprocessing.colors_extractor import get_image_color, get_colors_array, get_colors
from imgprocessing.image_size import ImageSize


def run_colors(df: pd.DataFrame, export_path: str):
    colors = []
    for _, row in tqdm(df.iterrows()):
        path = eval(row["thumbnail_path"])[-1]
        error = eval(row["error"])[-1]
        if not error:
            max_colors = get_image_color(path, get_colors_array(), get_colors())
            colors.append(max_colors)
        else:
            colors.append([])
    df["colors"] = colors
    df.to_csv(export_path, sep=";")


if __name__ == '__main__':
    size = ImageSize.maxresdefault.value
    images_path = os.path.join("..", "images")
    full_path = os.path.join("..", "colors", size)
    os.makedirs(full_path, exist_ok=True)
    gb_images = pd.read_csv(os.path.join(images_path, f"GB_{size}.csv"), sep=";", index_col=0)
    us_images = pd.read_csv(os.path.join(images_path, f"US_{size}.csv"), sep=";", index_col=0)
    names = [f"GB_{size}_colors.csv", f"US_{size}_colors.csv"]
    data = [gb_images, us_images]

    for df, name in zip(data, names):
        run_colors(df, os.path.join(full_path, name))
