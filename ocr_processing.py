import os
import cv2
import pytesseract

from argparse import ArgumentParser

from PIL import Image
from numpy import nan
from tqdm import tqdm

import pandas as pd

from images_downloading import ImageSize


def convert_to_png(jpg_path: str, png_dir: str, filename: str) -> None:
    img_convert = Image.open(jpg_path)
    img_convert.save(os.path.join(png_dir, filename))


def setup_args_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--size", help="Image size", type=ImageSize, choices=list(ImageSize),
                            default=ImageSize.maxresdefault.value)
    return arg_parser


def run_ocr(df, export_file_path: str, png_path) -> None:
    texts = []
    for _, row in tqdm(df.iterrows()):
        path = eval(row["thumbnail_path"])[-1]
        error = eval(row["error"])[-1]
        if not error:
            file_name = os.path.basename(path)[:-4] + ".png"
            convert_to_png(path, png_path, file_name)
            png_image_path = os.path.join(png_path, file_name)
            img = cv2.imread(png_image_path)
            text = pytesseract.image_to_string(img)
            texts.append(text)
        else:
            texts.append(nan)
    df["ocr_texts"] = texts
    df.to_csv(export_file_path, sep=";")


def main(args) -> None:
    images_path = "images"
    ocr_path = "ocr"
    size = args.size
    png_path = os.path.join(ocr_path, f"{size}")
    os.makedirs(png_path, exist_ok=True)
    gb_images = pd.read_csv(os.path.join(images_path, f"GB_{size}.csv"), sep=";", index_col=0)
    us_images = pd.read_csv(os.path.join(images_path, f"US_{size}.csv"), sep=";", index_col=0)
    names = [f"GB_{size}_ocr.csv", f"US_{size}_ocr.csv"]
    data = [gb_images, us_images]

    for df, name in zip(data, names):
        export_file_path = os.path.join(ocr_path, name)
        run_ocr(df, export_file_path, png_path)


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    parser = setup_args_parser()
    main(parser.parse_args())
