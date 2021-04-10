import os

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image

from object_detection.utils import label_map_util
from tqdm import tqdm

from images.images_downloading import ImageSize


def detect_objects(model, category_index, df: pd.DataFrame, file_name:str):
    min_score = 0.5
    image_size = (512, 512)
    all_names = []
    all_scores = []
    for _, row in tqdm(df.iterrows()):
        # print(row["thumbnail_path"])
        row_names = []
        row_scores = []
        for path, error in zip(eval(row["thumbnail_path"]), eval(row["error"])):
            if not error:
                # print(path)
                image = Image.open(path)
                array = tf.keras.preprocessing.image.img_to_array(image)
                array = array  # / 255.0
                array = tf.image.resize(array, image_size)
                array = np.array([array])
                results = model(array)
                result = {key: value.numpy() for key, value in results.items()}

                # label_id_offset = 0
                image_np_with_detections = array.copy()

                # image_np_with_detections = image_np_with_detections[0]
                scores = result['detection_scores'][0]
                scores = scores[scores > min_score]

                # boxes = result['detection_boxes'][0]
                # boxes = boxes[:scores.shape[0]]

                classes_ids = result['detection_classes'][0]
                classes_ids = classes_ids[:scores.shape[0]]
                classes_names = [category_index[class_id]['name'] for class_id in classes_ids]
                # print(classes_ids)
                # print(classes_names)
                # print(scores)
                for name, score in zip(classes_names, scores):
                    row_names.append(name)
                    row_scores.append(score)

                # print(boxes)
                # viz_utils.visualize_boxes_and_labels_on_image_array(
                #     image_np_with_detections,
                #     boxes,
                #     (classes_ids + label_id_offset).astype(int),
                #     scores,
                #     category_index,
                #     use_normalized_coordinates=True,
                #     max_boxes_to_draw=200,
                #     min_score_thresh=.30,
                #     agnostic_mode=False)
                #
                # plt.figure(figsize=(24, 32))
                # plt.imshow(image_np_with_detections.astype(dtype=np.int))
                # plt.savefig(f"abc_{row['number']}.png")
                # plt.show()
                # print("\n")
        all_names.append(row_names)
        all_scores.append(row_scores)
    df["obj_names"] = all_names
    df["obj_scores"] = all_scores
    df.to_csv(file_name, sep=";")


def main():
    # TODO args
    tf.get_logger().setLevel('ERROR')
    PATH_TO_LABELS = "mscoco_label_map.pbtxt"
    category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
    model_handle = "https://tfhub.dev/tensorflow/centernet/hourglass_512x512_kpts/1"
    print(tf.test.gpu_device_name())
    size = ImageSize.maxresdefault.value
    images_path = os.path.join("../images")
    us_images = pd.read_csv(os.path.join(images_path, f"US_{size}.csv"), sep=";", index_col=0)
    gb_images = pd.read_csv(os.path.join(images_path, f"GB_{size}.csv"), sep=";", index_col=0)
    names = [f"GB_{size}_object_detection.csv", f"US_{size}_object_detection.csv"]
    data = [gb_images, us_images]

    model = hub.load(model_handle)
    for df, name in zip(data, names):
        detect_objects(model, category_index, df, name)


if __name__ == '__main__':
    main()
