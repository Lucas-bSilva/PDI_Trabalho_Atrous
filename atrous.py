import numpy as np


def apply_activation(x, activation):
    """
    Aplica a função de ativação ao resultado da correlação.
    """
    if activation == "relu":
        return np.maximum(x, 0)
    return x


def atrous_correlation_rgb(img, kernel, r=1, stride=1, activation="identity"):
    """
    Aplica correlação espacial dilatada (à trous) em uma imagem RGB.

    A função processa os três canais da imagem (R, G e B) separadamente,
    sem uso de padding, e retorna o resultado em float32.
    """

    if img.dtype != np.uint8:
        raise ValueError("Imagem deve estar em uint8.")

    kernel = np.array(kernel, dtype=np.float32)
    m, n = kernel.shape

    H, W, C = img.shape

    # tamanho efetivo do kernel dilatado
    eff_h = 1 + (m - 1) * r
    eff_w = 1 + (n - 1) * r

    if H < eff_h or W < eff_w:
        raise ValueError("Kernel maior que imagem.")

    Hout = (H - eff_h) // stride + 1
    Wout = (W - eff_w) // stride + 1

    output = np.zeros((Hout, Wout, 3), dtype=np.float32)

    for c in range(3):  # R, G, B
        for i in range(Hout):
            for j in range(Wout):
                acc = 0.0
                for ki in range(m):
                    for kj in range(n):
                        y = i * stride + ki * r
                        x = j * stride + kj * r
                        acc += img[y, x, c] * kernel[ki, kj]

                output[i, j, c] = acc

    output = apply_activation(output, activation)
    return output