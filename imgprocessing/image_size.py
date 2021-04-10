from enum import Enum


class ImageSize(Enum):
    default = "default"
    hqdefault = "hqdefault"
    maxresdefault = "maxresdefault"

    def __str__(self):
        return self.value
