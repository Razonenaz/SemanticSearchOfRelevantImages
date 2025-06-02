from PIL import Image
import numpy as np

def prepare_image(image_path: str):
    image = Image.open(image_path).convert("RGB")
    return np.array(image)