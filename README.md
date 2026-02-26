# PDI – Sistema de Correlação Espacial Dilatada (À Trous)

##  Descrição

Este projeto implementa um sistema de **Processamento Digital de Imagens (PDI)** para aplicação de **operadores espaciais via correlação dilatada (à trous)** em imagens RGB.

O sistema foi desenvolvido conforme as diretrizes da disciplina de **Introdução ao Processamento Digital de Imagens**, respeitando as seguintes restrições acadêmicas:

- Implementação manual da correlação (sem uso de funções prontas como `cv2.filter2D` ou `scipy.signal`)
- Operação canal por canal (RGB)
- Máscaras carregadas via arquivos JSON
- Suporte à dilatação do kernel (parâmetro `r`)
- Suporte a stride
- Tratamento especial para operadores Sobel (valor absoluto + normalização 0–255)
- Sem padding (opera apenas na região válida)

---

##  Conceito Teórico

### Correlação Espacial

A correlação é definida como:

\[
g(x,y) = \sum_{i,j} f(x+i, y+j) \cdot h(i,j)
\]

onde:

- `f` é a imagem de entrada
- `h` é o kernel (máscara)
- `g` é a imagem resultante

---

### Correlação Dilatada (À Trous)

Na correlação dilatada, os elementos do kernel são espaçados por um fator `r`:

\[
g(x,y) = \sum_{i,j} f(x + r \cdot i, y + r \cdot j) \cdot h(i,j)
\]

Isso permite aumentar o campo receptivo sem aumentar o tamanho do kernel.

---

##  Estrutura do Projeto
PDI_TRABALHO_ATROUS
│
├── main.py # Interface de execução
├── atrous.py # Implementação da correlação dilatada
├── utils.py # Funções auxiliares
│
├── configs/
│ ├── gaussian5.json
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

Como Executar:

Sintaxe Geral

python main.py -i <imagem> -c <config.json> -o <saida> --show

Parâmetros:

Parâmetro	Descrição
-i	Imagem de entrada
-c	Arquivo JSON com definição do kernel
-o	Nome da imagem de saída
--show	Exibe a imagem resultante

 Exemplos de Execução:

 --- Filtro Gaussiano 5x5

python main.py -i Shapes.png -c configs/gaussian5.json -o saida_gauss.png --show

---- Filtro Box 10x10

python main.py -i testpat.1k.color2.tif -c configs/box_10x10.json -o saida_box.png --show

---- Sobel Horizontal

python main.py -i Shapes.png -c configs/sobel_h.json -o sobel_h.png --show

---- Sobel Vertical

python main.py -i Shapes.png -c configs/sobel_v.json -o sobel_v.png --show

 Estrutura dos Arquivos JSON:

Exemplo:

{
  "name": "gaussian_5x5",
  "r": 1,
  "stride": 1,
  "activation": "identity",
  "kernel": [...]
}

Campos
Campo	Função
kernel	Matriz da máscara
r	Fator de dilatação
stride	Passo da janela
activation	Função de ativação
is_sobel	Ativa pós-processamento específico


 Possibilidades de Teste

Alterar valor de r para testar dilatação

Alterar stride

Criar novos kernels via JSON

Comparar Sobel horizontal e vertical
