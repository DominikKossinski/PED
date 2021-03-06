import os

import pandas as pd

from imgprocessing.image_size import ImageSize
from helpers.files import load_csv, save_csv

if __name__ == '__main__':
    object_detection = os.path.join("..", "object_detection")
    size = ImageSize.maxresdefault.value
    gb_images = pd.read_csv(os.path.join(object_detection, f"GB_{size}_object_detection.csv"), sep=";", index_col=0)
    us_images = pd.read_csv(os.path.join(object_detection, f"US_{size}_object_detection.csv"), sep=";", index_col=0)

    ocr = os.path.join("..", "ocr")
    gb_ocr = pd.read_csv(os.path.join(ocr, f"GB_{size}_ocr.csv"), sep=";", index_col=0)
    us_ocr = pd.read_csv(os.path.join(ocr, f"US_{size}_ocr.csv"), sep=";", index_col=0)

    print(f"GB OCR: {gb_ocr.columns}")
    gb_images["ocr_texts"] = gb_ocr["ocr_texts"]
    us_images["ocr_texts"] = us_ocr["ocr_texts"]

    emotions = os.path.join("..", "emotions")
    emotions_path = os.path.join(emotions, size)
    gb_emotions = pd.read_csv(os.path.join(emotions_path, f"GB_{size}_emotions.csv"), sep=";", index_col=0)
    us_emotions = pd.read_csv(os.path.join(emotions_path, f"US_{size}_emotions.csv"), sep=";", index_col=0)
    print(f"Emotions: {gb_emotions.columns}")

    gb_images["emotions"] = gb_emotions["emotions"]
    us_images["emotions"] = us_emotions["emotions"]

    colors = "colors"
    colors_path = os.path.join("..", colors, size)
    gb_colors = pd.read_csv(os.path.join(colors_path, f"GB_{size}_colors.csv"), sep=";", index_col=0)
    us_colors = pd.read_csv(os.path.join(colors_path, f"US_{size}_colors.csv"), sep=";", index_col=0)
    print(f"Colors: {gb_colors.columns}")

    gb_images["colors"] = gb_colors["colors"]
    us_images["colors"] = us_colors["colors"]

    gb_cropped_colors, us_cropped_colors = load_csv(os.path.join("cropped_colors", size))
    gb_images["cropped_colors"] = gb_cropped_colors["colors"]
    us_images["cropped_colors"] = us_cropped_colors["colors"]
    print(f"Cropped colors: {gb_colors.columns}")

    print(gb_images.head())
    print(gb_images.columns)

    # images_path = os.path.join("..", )
    # os.makedirs(images_path, exist_ok=True)
    gb_images = gb_images.reset_index(drop=True)
    us_images = us_images.reset_index(drop=True)
    save_csv("images_data", [gb_images, us_images], ["GB_images_data", "US_images_data"])
