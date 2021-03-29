import os

import pandas as pd

from images_downloading import ImageSize

if __name__ == '__main__':
    object_detection = "object_detection"
    size = ImageSize.maxresdefault.value
    gb_images = pd.read_csv(os.path.join(object_detection, f"GB_{size}_{object_detection}.csv"), sep=";", index_col=0)
    us_images = pd.read_csv(os.path.join(object_detection, f"US_{size}_{object_detection}.csv"), sep=";", index_col=0)

    ocr = "ocr"
    gb_ocr = pd.read_csv(os.path.join(ocr, f"GB_{size}_{ocr}.csv"), sep=";", index_col=0)
    us_ocr = pd.read_csv(os.path.join(ocr, f"US_{size}_{ocr}.csv"), sep=";", index_col=0)

    print(f"GB OCR: {gb_ocr.columns}")
    gb_images["ocr_texts"] = gb_ocr["ocr_texts"]
    us_images["ocr_texts"] = us_ocr["ocr_texts"]

    emotions = "emotions"
    emotions_path = os.path.join(emotions, size)
    gb_emotions = pd.read_csv(os.path.join(emotions_path, f"GB_{size}_{emotions}.csv"), sep=";", index_col=0)
    us_emotions = pd.read_csv(os.path.join(emotions_path, f"US_{size}_{emotions}.csv"), sep=";", index_col=0)
    print(f"Emotions: {gb_emotions.columns}")

    gb_images["emotions"] = gb_emotions["emotions"]
    us_images["emotions"] = us_emotions["emotions"]

    colors = "colors"
    colors_path = os.path.join(colors, size)
    gb_colors = pd.read_csv(os.path.join(colors_path, f"GB_{size}_{colors}.csv"), sep=";", index_col=0)
    us_colors = pd.read_csv(os.path.join(colors_path, f"US_{size}_{colors}.csv"), sep=";", index_col=0)
    print(f"Emotions: {gb_colors.columns}")

    gb_images["colors"] = gb_colors["colors"]
    us_images["colors"] = us_colors["colors"]

    print(gb_images.head())
    print(gb_images.columns)

    images_path = "images_data"
    os.makedirs(images_path, exist_ok=True)
    gb_images.to_csv(os.path.join(images_path, "GB_images_data.csv"), sep=";")
    us_images.to_csv(os.path.join(images_path, "US_images_data.csv"), sep=";")
