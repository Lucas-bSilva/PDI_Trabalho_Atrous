import numpy as np


def apply_activation(x, activation):
    """
    Aplica uma função de ativação ao resultado da correlação.

    Esta função é utilizada após o cálculo da correlação para modificar
    os valores da imagem resultante de acordo com a função de ativação
    especificada.

    Parâmetros:
    x : numpy.ndarray
        Matriz contendo os valores resultantes da correlação.
    activation : str
        Tipo de função de ativação a ser aplicada. Atualmente suportado:
        - "relu": aplica a função ReLU (Rectified Linear Unit), que
          substitui valores negativos por zero.
        - "identity": mantém os valores originais sem alteração.

    Retorno:
    numpy.ndarray
        Matriz com a função de ativação aplicada.
    """
    if activation == "relu":
        return np.maximum(x, 0)
    return x


def atrous_correlation_rgb(img, kernel, r=1, stride=1, activation="identity"):
    """
    Realiza a correlação espacial dilatada (à trous) em uma imagem RGB.

    Esta função aplica manualmente um operador de correlação utilizando
    um kernel (máscara) sobre uma imagem colorida de 24 bits (RGB).
    A operação considera dilatação do kernel (parâmetro r), permitindo
    ampliar o campo receptivo sem aumentar o tamanho da máscara.

    O processamento é realizado canal por canal (R, G e B) e sem uso
    de padding, conforme as restrições do projeto.

    Parâmetros:
    img : numpy.ndarray
        Imagem de entrada no formato RGB com tipo uint8.
    kernel : list ou numpy.ndarray
        Matriz que representa a máscara de correlação.
    r : int, opcional
        Fator de dilatação do kernel. Define o espaçamento entre os
        elementos da máscara durante a correlação. Padrão = 1.
    stride : int, opcional
        Passo de deslocamento da janela de correlação sobre a imagem.
        Padrão = 1.
    activation : str, opcional
        Função de ativação aplicada após a correlação. Pode ser:
        - "identity": mantém os valores calculados
        - "relu": substitui valores negativos por zero

    Retorno:
    numpy.ndarray
        Imagem resultante da correlação, convertida novamente para
        o formato uint8 no intervalo [0,255].

    Exceções:
    ValueError
        Lançada caso a imagem não esteja no formato uint8 ou caso
        o kernel seja maior que a imagem considerando a dilatação.
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

    output = np.clip(output, 0, 255)
    return output.astype(np.uint8)