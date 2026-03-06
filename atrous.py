import numpy as np  # Importa a biblioteca NumPy para manipulação eficiente de arrays numéricos


def apply_activation(x, activation):  # Define a função que aplica uma função de ativação ao resultado da correlação
    """
    Aplica uma funcao de ativacao ao resultado da correlacao.

    Esta funcao é utilizada após o calculo da correlacao para modificar
    os valores da imagem resultante de acordo com a funcao de ativacao
    especificada.

    Parâmetros:
    x : numpy.ndarray
        Matriz contendo os valores resultantes da correlacao.
    activation : str
        Tipo de funcao de ativacao a ser aplicada. Atualmente suportado:
        - "relu": aplica a funcao ReLU (Rectified Linear Unit), que
          substitui valores negativos por zero.
        - "identity": mantém os valores originais sem alteracao.

    Retorno:
    numpy.ndarray
        Matriz com a funcao de ativacao aplicada.
    """
    if activation == "relu":  # Verifica se a ativação escolhida é ReLU
        return np.maximum(x, 0)  # Aplica ReLU: substitui valores negativos por 0
    return x  # Caso não seja ReLU, retorna os valores originais sem modificação


def atrous_correlation_rgb(img, kernel, r=1, stride=1, activation="identity"):  # Define a função principal de correlação Atrous em imagem RGB
    """
    Realiza a correlacao espacial dilatada (à trous) em uma imagem RGB.

    Esta funcao aplica manualmente um operador de correlacao utilizando
    um kernel (mascara) sobre uma imagem colorida de 24 bits (RGB).
    A operacao considera dilatacao do kernel (parâmetro r), permitindo
    ampliar o campo receptivo sem aumentar o tamanho da mascara.

    O processamento é realizado canal por canal (R, G e B) e sem uso
    de padding, conforme as restrições do projeto.

    Parâmetros:
    img : numpy.ndarray
        Imagem de entrada no formato RGB com tipo uint8.
    kernel : list ou numpy.ndarray
        Matriz que representa a mascara de correlacao.
    r : int, opcional
        Fator de dilatacao do kernel. Define o espaçamento entre os
        elementos da mascara durante a correlacao. Padrão = 1.
    stride : int, opcional
        Passo de deslocamento da janela de correlacao sobre a imagem.
        Padrão = 1.
    activation : str, opcional
        Funcao de ativacao aplicada após a correlacao.

    Retorno:
    numpy.ndarray
        Imagem resultante da correlacao.
    """

    if img.dtype != np.uint8:  # Verifica se a imagem está no tipo uint8 (formato padrão de imagens)
        raise ValueError("Imagem deve estar em uint8.")  # Lança erro caso o tipo esteja incorreto

    kernel = np.array(kernel, dtype=np.float32)  # Converte o kernel para um array NumPy do tipo float32
    m, n = kernel.shape  # Obtém o número de linhas (m) e colunas (n) do kernel

    H, W, C = img.shape  # Obtém altura (H), largura (W) e número de canais (C) da imagem

    # tamanho efetivo do kernel dilatado
    eff_h = 1 + (m - 1) * r  # Calcula a altura efetiva do kernel considerando o fator de dilatação r
    eff_w = 1 + (n - 1) * r  # Calcula a largura efetiva do kernel considerando o fator de dilatação r

    if H < eff_h or W < eff_w:  # Verifica se o kernel dilatado cabe dentro da imagem
        raise ValueError("Kernel maior que imagem.")  # Lança erro caso o kernel seja maior que a imagem

    Hout = (H - eff_h) // stride + 1  # Calcula a altura da imagem de saída considerando o stride
    Wout = (W - eff_w) // stride + 1  # Calcula a largura da imagem de saída considerando o stride

    output = np.zeros((Hout, Wout, 3), dtype=np.float32)  # Cria uma matriz de saída inicializada com zeros

    for c in range(3):  # Percorre os três canais da imagem (R, G e B)
        for i in range(Hout):  # Percorre todas as posições verticais possíveis na imagem de saída
            for j in range(Wout):  # Percorre todas as posições horizontais possíveis na imagem de saída
                acc = 0.0  # Inicializa o acumulador que armazenará o valor da correlação
                for ki in range(m):  # Percorre as linhas do kernel
                    for kj in range(n):  # Percorre as colunas do kernel
                        y = i * stride + ki * r  # Calcula a posição vertical na imagem original
                        x = j * stride + kj * r  # Calcula a posição horizontal na imagem original
                        acc += img[y, x, c] * kernel[ki, kj]  # Multiplica o pixel pelo valor do kernel e acumula

                output[i, j, c] = acc  # Armazena o valor final calculado na posição correspondente da saída

    output = apply_activation(output, activation)  # Aplica a função de ativação ao resultado da correlação

    # output = np.clip(output, 0, 255)  # Linha comentada: limitaria os valores da imagem entre 0 e 255
    # return output.astype(np.uint8)  # Linha comentada: converteria o resultado para formato uint8

    return output  # Retorna a matriz resultante sem conversão para uint8