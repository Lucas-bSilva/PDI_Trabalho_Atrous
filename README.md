# PDI – Sistema de Correlação Espacial Dilatada (À Trous)

Projeto desenvolvido para a disciplina **Introdução ao Processamento Digital de Imagens**  
Centro de Informática – **Universidade Federal da Paraíba (UFPB)**

---

# Descrição

Este projeto implementa um sistema de **Processamento Digital de Imagens (PDI)** para aplicação de **operadores espaciais utilizando correlação dilatada (À Trous)** em imagens RGB de 24 bits.

O sistema foi desenvolvido respeitando as restrições acadêmicas da disciplina, incluindo:

- Implementação **manual da correlação espacial**
- Proibição do uso de funções prontas como `cv2.filter2D` ou `scipy.signal`
- Processamento **canal por canal (RGB)**
- Máscaras configuráveis por meio de **arquivos JSON**
- Suporte à dilatação do kernel (`r`)
- Suporte ao parâmetro `stride`
- Pós-processamento específico para operadores **Sobel**
- Execução **sem uso de padding**

---

# Objetivo do Projeto

Desenvolver um sistema de processamento digital de imagens capaz de aplicar **operadores espaciais utilizando correlação dilatada (À Trous)** em imagens RGB, permitindo a experimentação com diferentes filtros espaciais por meio de **configurações externas definidas em arquivos JSON**.

Além disso, o projeto permite avaliar o comportamento visual de filtros de suavização e operadores de detecção de bordas em **duas imagens de teste**, analisando o efeito dos parâmetros `r` e `stride` sobre a imagem resultante.

---

# Fundamentação Teórica

## Correlação Espacial

A correlação espacial consiste na aplicação de uma máscara (kernel) sobre uma imagem, realizando uma soma ponderada dos pixels da vizinhança.

\[
g(x,y) = \sum_{i,j} f(x+i, y+j) \cdot h(i,j)
\]

Onde:

- `f` → imagem de entrada  
- `h` → kernel (máscara)  
- `g` → imagem resultante  

---

## Correlação Dilatada (À Trous)

A correlação dilatada introduz um fator de espaçamento entre os elementos do kernel.

\[
g(x,y) = \sum_{i,j} f(x + r \cdot i, y + r \cdot j) \cdot h(i,j)
\]

Onde:

- `r` é o **fator de dilatação (dilation rate)**.

Esse parâmetro permite aumentar o **campo receptivo da operação** sem aumentar o tamanho do kernel.

---

# Arquitetura do Sistema

O sistema foi dividido em quatro arquivos principais.

## main.py

Responsável por:

- leitura dos argumentos da linha de comando
- carregamento da imagem de entrada
- leitura do arquivo de configuração JSON
- execução da correlação dilatada
- separação entre filtros comuns e operadores Sobel
- salvamento da imagem resultante
- exibição opcional do resultado

---

## atrous.py

Implementa o **algoritmo principal de correlação dilatada**, incluindo:

- aplicação manual do kernel
- suporte à dilatação (`r`)
- suporte ao parâmetro `stride`
- processamento independente dos canais **R, G e B**
- aplicação opcional de função de ativação

O resultado da correlação é retornado em **float**, permitindo tratamento correto dos operadores Sobel antes da conversão final para imagem.

---

## utils.py

Contém funções auxiliares utilizadas no projeto:

- `histogram_stretch()` → normalização de intensidade
- `sobel_postprocess()` → aplicação de valor absoluto + expansão de histograma
- `to_uint8_clip()` → conversão dos filtros comuns para o intervalo `[0,255]`

---

## run_all_tests.py

Arquivo opcional utilizado para **automatizar a execução dos 12 testes** exigidos no projeto.

Esse arquivo não altera o algoritmo de processamento, apenas executa em sequência os comandos que poderiam ser rodados manualmente no terminal.

---

# Estrutura do Projeto

```text
PDI_TRABALHO_ATROUS/
│
├── main.py
├── atrous.py
├── utils.py
├── run_all_tests.py
│
├── configs/
│   ├── gaussian5.json
│   ├── box_1x10.json
│   ├── box_10x1.json
│   ├── box_10x10.json
│   ├── sobel_h.json
│   └── sobel_v.json
│
├── Shapes.png
├── testpat.1k.color2.tif
│
├── outputs/
│
└── README.md
```

---

# Requisitos

Instalar as dependências necessárias:

```bash
pip install numpy pillow
```

---

# Como Executar

## Sintaxe geral

```bash
python main.py -i <imagem> -c <config.json> -o <saida> --show
```

## Parâmetros

| Parâmetro | Descrição |
|-----------|-----------|
| `-i` | imagem de entrada |
| `-c` | arquivo JSON contendo o kernel |
| `-o` | nome da imagem de saída |
| `--show` | exibe a imagem original e o resultado |

---

# Testes Solicitados

De acordo com a interpretação mais completa do enunciado, foram realizados **12 testes**, correspondentes à aplicação dos **6 filtros solicitados nas 2 imagens fornecidas pelo professor**.

---

## Testes na imagem `Shapes.png`

### 1️ Gaussian 5x5

```bash
python main.py -i Shapes.png -c configs/gaussian5.json -o outputs/shapes_gaussian5.png --show
```

### 2️ Box 1x10 (suavização horizontal)

```bash
python main.py -i Shapes.png -c configs/box_1x10.json -o outputs/shapes_box_1x10.png --show
```

### 3️ Box 10x1 (suavização vertical)

```bash
python main.py -i Shapes.png -c configs/box_10x1.json -o outputs/shapes_box_10x1.png --show
```

### 4️ Box 10x10

```bash
python main.py -i Shapes.png -c configs/box_10x10.json -o outputs/shapes_box_10x10.png --show
```

### 5️ Sobel Horizontal

```bash
python main.py -i Shapes.png -c configs/sobel_h.json -o outputs/shapes_sobel_h.png --show
```

### 6️ Sobel Vertical

```bash
python main.py -i Shapes.png -c configs/sobel_v.json -o outputs/shapes_sobel_v.png --show
```

---

## Testes na imagem `testpat.1k.color2.tif`

### 7️ Gaussian 5x5

```bash
python main.py -i testpat.1k.color2.tif -c configs/gaussian5.json -o outputs/testpat_gaussian5.png --show
```

### 8️ Box 1x10 (suavização horizontal)

```bash
python main.py -i testpat.1k.color2.tif -c configs/box_1x10.json -o outputs/testpat_box_1x10.png --show
```

### 9️ Box 10x1 (suavização vertical)

```bash
python main.py -i testpat.1k.color2.tif -c configs/box_10x1.json -o outputs/testpat_box_10x1.png --show
```

### 10 Box 10x10

```bash
python main.py -i testpat.1k.color2.tif -c configs/box_10x10.json -o outputs/testpat_box_10x10.png --show
```

### 1️1️ Sobel Horizontal

```bash
python main.py -i testpat.1k.color2.tif -c configs/sobel_h.json -o outputs/testpat_sobel_h.png --show
```

### 1️2️ Sobel Vertical

```bash
python main.py -i testpat.1k.color2.tif -c configs/sobel_v.json -o outputs/testpat_sobel_v.png --show
```

---

# Execução Automática dos 12 Testes

Caso se deseje automatizar a geração de todos os resultados, pode-se utilizar o arquivo:

```bash
python run_all_tests.py
```

Esse script executa, em sequência, os 12 testes descritos acima e salva automaticamente os arquivos na pasta `outputs/`.

---

# Estrutura dos Arquivos JSON

Exemplo de configuração de filtro:

```json
{
  "name": "gaussian_5x5",
  "r": 1,
  "stride": 1,
  "activation": "identity",
  "kernel": [...]
}
```

## Campos

| Campo | Função |
|-------|--------|
| `kernel` | matriz da máscara |
| `r` | fator de dilatação |
| `stride` | passo da janela |
| `activation` | função de ativação |
| `is_sobel` | ativa pós-processamento Sobel |

---

# Resultados

Os filtros foram aplicados às duas imagens fornecidas no enunciado, totalizando **12 saídas experimentais**.

Esses resultados permitem comparar:

- filtros de suavização isotrópica
- filtros de suavização direcional
- filtros de detecção de bordas
- comportamento em imagens geométricas simples
- comportamento em imagem colorida com regiões de alta frequência espacial

---

# Análise dos Resultados

Os resultados obtidos demonstram o comportamento esperado dos filtros aplicados.

- O parâmetro **r** aumenta o campo receptivo da operação de correlação.
- O **stride** altera a densidade de amostragem da imagem resultante.
- Filtros **Box** realizam suavização baseada em média uniforme da vizinhança.
- O filtro **Gaussian** suaviza a imagem preservando melhor as bordas.
- Operadores **Sobel** detectam bordas horizontais e verticais por meio da aproximação do gradiente da imagem.

Para os filtros Sobel é aplicado um pós-processamento composto por:

- cálculo do **valor absoluto do gradiente**
- **expansão linear do histograma para o intervalo [0,255]**

Esse procedimento foi adotado para atender rigorosamente à exigência do enunciado, que determina o tratamento adequado dos valores negativos gerados pelo operador Sobel antes da exibição.

---