import numpy as np

def histogram_stretch(channel):
    min_val = np.min(channel)
    max_val = np.max(channel)

    if max_val - min_val == 0:
        return np.zeros_like(channel)

    stretched = (channel - min_val) * (255.0 / (max_val - min_val))
    return np.clip(stretched, 0, 255).astype(np.uint8)

def sobel_postprocess(img):
    img = np.abs(img.astype(np.float32))
    result = np.zeros_like(img, dtype=np.uint8)

    for c in range(3):
        result[:, :, c] = histogram_stretch(img[:, :, c])

    return result