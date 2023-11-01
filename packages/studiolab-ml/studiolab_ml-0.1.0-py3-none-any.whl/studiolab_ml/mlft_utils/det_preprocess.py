import numpy as np
from PIL import Image

from .bbox import letterbox

def detection_preprocess(
        image: Image.Image, 
        target_size: int
    ):
    if isinstance(image, Image.Image):
        pass
    else:
        raise TypeError('image must be PIL Image')
    # resize image and pad
    image, ratio, (dw, dh), img_size = letterbox(image, new_shape=(target_size, target_size), stride=32)

    # normalize image
    img_array = np.array(image).astype(np.float32) / 255.0

    # transpose image to NCHW format
    img_array = img_array.transpose((2, 0, 1))
    img_array = np.expand_dims(img_array, axis=0)

    return img_array.astype(np.float32), (ratio, (dw, dh), img_size)