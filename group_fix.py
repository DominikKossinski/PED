import os
import pandas as pd
from images_downloading import ImageSize

size = ImageSize.maxresdefault.value
images_path = os.path.join("images")
for size in list(ImageSize):
    gb_images = pd.read_pickle(os.path.join(images_path, f"GB_{size}.plk"))
    us_images = pd.read_pickle(os.path.join(images_path, f"US_{size}.plk"))

    gb_images.to_csv(os.path.join(images_path, f"GB_{size}.csv"), sep=";")
    us_images.to_csv(os.path.join(images_path, f"US_{size}.csv"), sep=";")
