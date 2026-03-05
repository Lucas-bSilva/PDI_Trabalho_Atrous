import argparse
import json
import numpy as np
from PIL import Image
import tkinter as tk
from PIL import ImageTk

from atrous import atrous_correlation_rgb
from utils import sobel_postprocess


def load_config(path):
    """
    Carrega o arquivo de configuração JSON contendo os parâmetros
    do filtro (kernel, dilatação, stride, ativação e flags opcionais).
    """
    with open(path, 'r') as f:
        return json.load(f)


def show_images(original, result, title="Resultado"):
    """
    Exibe a imagem original e a imagem resultante lado a lado
    em uma janela gráfica utilizando Tkinter.
    """
    root = tk.Tk()
    root.title(title)

    original_img = Image.fromarray(original)
    result_img = Image.fromarray(result)

    width = original_img.width + result_img.width
    height = max(original_img.height, result_img.height)

    combined = Image.new("RGB", (width, height))
    combined.paste(original_img, (0, 0))
    combined.paste(result_img, (original_img.width, 0))

    tk_img = ImageTk.PhotoImage(combined)
    label = tk.Label(root, image=tk_img)
    label.pack()

    root.mainloop()


def main():
    """
    Função principal do programa.

    Responsável por:
    - Ler argumentos da linha de comando
    - Carregar imagem de entrada
    - Carregar configuração do filtro
    - Executar a correlação dilatada
    - Aplicar pós-processamento Sobel (quando necessário)
    - Salvar a imagem resultante
    - Exibir o resultado opcionalmente
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-c", "--config", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--show", action="store_true")

    args = parser.parse_args()

    img = Image.open(args.input).convert("RGB")
    img_np = np.array(img, dtype=np.uint8)

    config = load_config(args.config)

    result = atrous_correlation_rgb(
        img_np,
        kernel=config["kernel"],
        r=config["r"],
        stride=config["stride"],
        activation=config["activation"]
    )

    # aplica pós-processamento específico caso o filtro seja Sobel
    if config.get("is_sobel", False):
        result = sobel_postprocess(result)

    Image.fromarray(result).save(args.output)

    # exibe as imagens caso a flag --show seja utilizada
    if args.show:
        show_images(img_np, result, config["name"])


if __name__ == "__main__":
    main()