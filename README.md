# PDI – Sistema de Correlação Espacial Dilatada (À Trous)

##  Descrição

Este projeto implementa um sistema de **Processamento Digital de Imagens (PDI)** para aplicação de **operadores espaciais via correlação dilatada (À Trous)** em imagens RGB de 24 bits.

O sistema foi desenvolvido conforme as diretrizes da disciplina de **Introdução ao Processamento Digital de Imagens**, respeitando as seguintes restrições acadêmicas:

- Implementação manual da correlação (sem uso de funções prontas como `cv2.filter2D` ou `scipy.signal`)
- Operação canal por canal (RGB)
- Máscaras carregadas via arquivos JSON
- Suporte à dilatação do kernel (`r`)
- Suporte a `stride`
- Tratamento especial para operadores Sobel (valor absoluto + normalização para [0,255])
- Sem uso de padding (opera apenas na região válida)

---

##  Conceito Teórico

### 🔹 Correlação Espacial

\[
g(x,y) = \sum_{i,j} f(x+i, y+j) \cdot h(i,j)
\]

Onde:
- `f` = imagem de entrada
- `h` = kernel (máscara)
- `g` = imagem resultante

---

### 🔹 Correlação Dilatada (À Trous)

\[
g(x,y) = \sum_{i,j} f(x + r \cdot i, y + r \cdot j) \cdot h(i,j)
\]

O parâmetro `r` aumenta o campo receptivo sem aumentar o tamanho do kernel.

---

##  Estrutura do Projeto

PDI_TRABALHO_ATROUS/
│
├── main.py
├── atrous.py
├── utils.py
│
├── configs/
│ ├── gaussian5.json
│ ├── box_1x10.json
│ ├── box_10x1.json
│ ├── box_10x10.json
│ ├── sobel_h.json
│ └── sobel_v.json
│
├── Shapes.png
├── testpat.1k.color2.tif
└── README.md


---

##  Requisitos

Instalar dependências:

```bash
pip install numpy pillow

 Como Executar

🔹 Sintaxe Geral

python main.py -i <imagem> -c <config.json> -o <saida> --show

🔹 Parâmetros

| Parâmetro | Descrição                            |
| --------- | ------------------------------------ |
| `-i`      | Imagem de entrada                    |
| `-c`      | Arquivo JSON com definição do kernel |
| `-o`      | Nome da imagem de saída              |
| `--show`  | Exibe imagem original e resultado    |


Testes Solicitados:

1️ Gaussian 5x5:

python main.py -i Shapes.png -c configs/gaussian5.json -o saida_gauss.png --show


2️ Box 1x10 (suavização horizontal):

python main.py -i Shapes.png -c configs/box_1x10.json -o saida_box_1x10.png --show

3️ Box 10x1 (suavização vertical):

python main.py -i Shapes.png -c configs/box_10x1.json -o saida_box_10x1.png --show

4️ Box 10x10:

python main.py -i testpat.1k.color2.tif -c configs/box_10x10.json -o saida_box_10x10.png --show

5️ Sobel Horizontal:

python main.py -i Shapes.png -c configs/sobel_h.json -o saida_sobel_h.png --show

6️ Sobel Vertical:

python main.py -i Shapes.png -c configs/sobel_v.json -o saida_sobel_v.png --show


Estrutura dos Arquivos JSON

Exemplo:

{
  "name": "gaussian_5x5",
  "r": 1,
  "stride": 1,
  "activation": "identity",
  "kernel": [...]
}

Campos:

| Campo        | Função                             |
| ------------ | ---------------------------------- |
| `kernel`     | Matriz da máscara                  |
| `r`          | Fator de dilatação (1 a 5)         |
| `stride`     | Passo da janela (1 a 5)            |
| `activation` | identity ou relu                   |
| `is_sobel`   | Ativa pós-processamento específico |


 -- Análise dos Resultados:

A variação do parâmetro r aumenta o campo receptivo.

O stride altera a densidade da amostragem.

Filtros Box realizam suavização.

Gaussian suaviza preservando melhor as bordas.

Sobel detecta bordas (horizontal ou vertical).

-- Para Sobel é aplicado:

   valor absoluto

   normalização para intervalo [0,255]
