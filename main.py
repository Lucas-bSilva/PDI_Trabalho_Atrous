import argparse
import json
import os
import numpy as np
from PIL import Image
import tkinter as tk
from PIL import ImageTk

from atrous import atrous_correlation_rgb
from utils import sobel_postprocess, to_uint8_clip


def load_config(path):
    """
    Carrega o arquivo JSON com os parâmetros do filtro.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def show_images(original, result, title="Resultado"):
    """
    Exibe a imagem original e o resultado lado a lado.
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

    # se for Sobel, aplica valor absoluto + normalização
    if config.get("is_sobel", False):
        result = sobel_postprocess(result)
    else:
        result = to_uint8_clip(result)

    # cria a pasta de saída se necessário
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    Image.fromarray(result).save(args.output)

    if args.show:
        show_images(img_np, result, config["name"])


if __name__ == "__main__":
    main()