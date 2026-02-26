import argparse
import json
import numpy as np
from PIL import Image
import tkinter as tk
from PIL import ImageTk

from atrous import atrous_correlation_rgb
from utils import sobel_postprocess

def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def show_images(original, result, title="Resultado"):
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

    if config.get("is_sobel", False):
        result = sobel_postprocess(result)

    Image.fromarray(result).save(args.output)

    if args.show:
        show_images(img_np, result, config["name"])

if __name__ == "__main__":
    main()