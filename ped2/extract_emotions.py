import os
from argparse import ArgumentParser

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from imgprocessing.image_size import ImageSize
from imgprocessing.emotions_detector import EmotionDetector


def setup_args_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--size", help="Image size", type=ImageSize, choices=list(ImageSize),
                            default=ImageSize.default.value)
    return arg_parser


def run_emotions(df, export_path, detector: EmotionDetector) -> None:
    emotions = []
    for _, row in tqdm(df.iterrows()):
        path = eval(row["thumbnail_path"])[-1]
        error = eval(row["error"])[-1]
        if not error:
            img = cv2.imread(path)
            img = np.array(img)
            e = detector.call(img)
            emotions.append(e)
        else:
            emotions.append([])
    df["emotions"] = emotions
    df.to_csv(export_path, sep=";")


def main(args):
    detector = EmotionDetector()
    images_path = os.path.join("..", "images")
    emotion_path = os.path.join("..", "emotions")
    size = args.size.value
    full_path = os.path.join(emotion_path, size)
    os.makedirs(full_path, exist_ok=True)
    gb_images = pd.read_csv(os.path.join(images_path, f"GB_{size}.csv"), sep=";", index_col=0)
    us_images = pd.read_csv(os.path.join(images_path, f"US_{size}.csv"), sep=";", index_col=0)
    names = [f"GB_{size}_emotions.csv", f"US_{size}_emotions.csv"]
    data = [gb_images, us_images]

    for df, name in zip(data, names):
        run_emotions(df, os.path.join(full_path, name), detector)


if __name__ == '__main__':
    parser = setup_args_parser()
    main(parser.parse_args())
