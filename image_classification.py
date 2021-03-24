import os
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

from images_downloading import ImageSize


def get_top_k(classes, scores, k):
    top_classes = classes.numpy()[:k]
    names = []
    print(f"Top classes: {top_classes}")
    # for c in top_classes:
    #     names.append(classes_names[c]) TODO
    return names, scores.numpy()[:k]


if __name__ == '__main__':
    print(tf.test.gpu_device_name())
    size = ImageSize.maxresdefault.value
    images_path = os.path.join("images")
    gb_images = pd.read_pickle(os.path.join(images_path, f"GB_{size}.plk"))
    us_images = pd.read_pickle(os.path.join(images_path, f"US_{size}.plk"))
    k = 5
    image_size = (1024, 1024)
    # model = tf.keras.applications.resnet50.ResNet50()
    print("ok")
    detector = hub.load("https://tfhub.dev/tensorflow/faster_rcnn/inception_resnet_v2_1024x1024/1")

    for _, row in gb_images.iterrows():
        for path, error in zip(row["thumbnail_path"], row["error"]):
            if not error:
                print(path)
                image = Image.open(path)
                array = tf.keras.preprocessing.image.img_to_array(image)
                # array = array  # / 255.0
                # array = tf.image.resize(array, size)
                array = np.array([array])
                detector_output = detector(array)
                print(detector_output.keys())
                det_scores = detector_output["detection_scores"][0]
                class_ids = detector_output["detection_classes"][0]
                detection_boxes = detector_output["detection_boxes"][0]
                names, scores = get_top_k(class_ids, det_scores, 5)
                # pred = model.predict(array)
                # top_k = tf.keras.applications.resnet50.decode_predictions(pred, k)[0]
                # classes = list(map(lambda x: (x[1], x[2] * 100), top_k))
                image.show()
                print(names)
                print(scores)
                print(detection_boxes)
                print("\n")
                input()
        if row["number"] == 20:
            break
