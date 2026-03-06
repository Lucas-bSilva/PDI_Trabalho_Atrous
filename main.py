import argparse  # Importa a biblioteca para ler argumentos passados pela linha de comando
import json  # Importa a biblioteca para manipular arquivos no formato JSON
import numpy as np  # Importa o NumPy para trabalhar com arrays numéricos
from PIL import Image  # Importa a classe Image da PIL para abrir, converter e salvar imagens
import tkinter as tk  # Importa o Tkinter para criar janelas gráficas
from PIL import ImageTk  # Importa ImageTk para exibir imagens PIL dentro da interface Tkinter

from atrous import atrous_correlation_rgb  # Importa a função que aplica a correlação dilatada na imagem RGB
from utils import sobel_postprocess  # Importa a função de pós-processamento para o filtro de Sobel


def load_config(path):  # Define a função que carrega o arquivo de configuração
    """
    Carrega o arquivo de configuracao JSON contendo os parâmetros
    do filtro (kernel, dilatacao, stride, ativacao e flags opcionais).
    """  # Docstring explicando a finalidade da função
    with open(path, 'r') as f:  # Abre o arquivo JSON no modo leitura
        return json.load(f)  # Lê o conteúdo JSON e retorna como dicionário Python


def show_images(original, result, title="Resultado"):  # Define a função que mostra as imagens na tela
    """
    Exibe a imagem original e a imagem resultante lado a lado
    em uma janela gráfica utilizando Tkinter.
    """  # Docstring explicando a função
    root = tk.Tk()  # Cria a janela principal da interface gráfica
    root.title(title)  # Define o título da janela

    original_img = Image.fromarray(original)  # Converte o array NumPy da imagem original para imagem PIL
    result_img = Image.fromarray(result)  # Converte o array NumPy da imagem resultante para imagem PIL

    width = original_img.width + result_img.width  # Soma as larguras das duas imagens para colocá-las lado a lado
    height = max(original_img.height, result_img.height)  # Define a altura da imagem combinada como a maior entre as duas

    combined = Image.new("RGB", (width, height))  # Cria uma nova imagem vazia que irá armazenar as duas imagens juntas
    combined.paste(original_img, (0, 0))  # Cola a imagem original no lado esquerdo da imagem combinada
    combined.paste(result_img, (original_img.width, 0))  # Cola a imagem resultante à direita da original

    tk_img = ImageTk.PhotoImage(combined)  # Converte a imagem combinada para o formato aceito pelo Tkinter
    label = tk.Label(root, image=tk_img)  # Cria um componente visual para exibir a imagem na janela
    label.pack()  # Adiciona o componente à janela

    root.mainloop()  # Inicia o loop da interface gráfica e mantém a janela aberta


def main():  # Define a função principal do programa
    """
    Funcao principal do programa.

    Responsável por:
    - Ler argumentos da linha de comando
    - Carregar imagem de entrada
    - Carregar configuracao do filtro
    - Executar a correlacao dilatada
    - Aplicar pos-processamento Sobel (quando necessário)
    - Salvar a imagem resultante
    - Exibir o resultado opcionalmente
    """  # Docstring explicando o fluxo principal do programa
    parser = argparse.ArgumentParser()  # Cria o objeto responsável por interpretar os argumentos da linha de comando
    parser.add_argument("-i", "--input", required=True)  # Define o argumento obrigatório para o arquivo de imagem de entrada
    parser.add_argument("-c", "--config", required=True)  # Define o argumento obrigatório para o arquivo de configuração JSON
    parser.add_argument("-o", "--output", required=True)  # Define o argumento obrigatório para o caminho da imagem de saída
    parser.add_argument("--show", action="store_true")  # Define uma flag opcional para exibir as imagens após o processamento

    args = parser.parse_args()  # Lê os argumentos informados pelo usuário no terminal

    img = Image.open(args.input).convert("RGB")  # Abre a imagem de entrada e converte para o formato RGB
    img_np = np.array(img, dtype=np.uint8)  # Converte a imagem PIL em array NumPy do tipo uint8

    config = load_config(args.config)  # Carrega os parâmetros do filtro a partir do arquivo JSON

    result = atrous_correlation_rgb(  # Chama a função principal de correlação dilatada
        img_np,  # Passa a imagem de entrada em formato NumPy
        kernel=config["kernel"],  # Passa o kernel definido no arquivo de configuração
        r=config["r"],  # Passa o valor de dilatação do kernel
        stride=config["stride"],  # Passa o passo de deslocamento do kernel
        activation=config["activation"]  # Passa a função de ativação a ser usada no resultado
    )  # Finaliza a chamada da função e armazena o resultado

    # aplica pós-processamento específico caso o filtro seja Sobel
    if config.get("is_sobel", False):  # Verifica se a configuração indica que o filtro Sobel deve ser aplicado
        result = sobel_postprocess(result)  # Aplica o pós-processamento Sobel no resultado
    else:  # Caso não seja um filtro Sobel
        # ADICIONE ESTA PARTE: 
        # Para filtros normais (Gauss, Box), limita e converte agora
        result = np.clip(result, 0, 255).astype(np.uint8)  # Limita os valores entre 0 e 255 e converte para uint8

    Image.fromarray(result).save(args.output)  # Converte o resultado para imagem e salva no caminho especificado

    # exibe as imagens caso a flag --show seja utilizada
    if args.show:  # Verifica se o usuário ativou a opção de mostrar as imagens
        show_images(img_np, result, config["name"])  # Exibe a imagem original e a resultante lado a lado


if __name__ == "__main__":  # Verifica se este arquivo está sendo executado diretamente
    main()  # Chama a função principal do programa