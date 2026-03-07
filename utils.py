import numpy as np


def histogram_stretch(channel):
    """
    Realiza expansão linear do histograma, normalizando os valores
    para o intervalo [0,255].
    """
    min_val = np.min(channel)
    max_val = np.max(channel)

    if max_val - min_val == 0:
        return np.zeros_like(channel, dtype=np.uint8)

    stretched = (channel - min_val) * (255.0 / (max_val - min_val))
    return np.clip(stretched, 0, 255).astype(np.uint8)


def sobel_postprocess(img):
    """
    Pós-processamento para filtros Sobel:
    - aplica valor absoluto
    - aplica expansão de histograma em cada canal
    """
    img = np.abs(img.astype(np.float32))
    result = np.zeros_like(img, dtype=np.uint8)

    for c in range(3):
        result[:, :, c] = histogram_stretch(img[:, :, c])

    return result


def to_uint8_clip(img):
    """
    Converte a saída da correlação comum para uint8,
    limitando os valores ao intervalo [0,255].
    """
    return np.clip(img, 0, 255).astype(np.uint8)