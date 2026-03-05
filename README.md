# PDI – Sistema de Correlação Espacial Dilatada (À Trous)

## Descrição

Este projeto implementa um sistema de **Processamento Digital de Imagens (PDI)** para aplicação de **operadores espaciais via correlação dilatada (À Trous)** em imagens RGB de 24 bits.

O sistema foi desenvolvido conforme as diretrizes da disciplina de **Introdução ao Processamento Digital de Imagens**, respeitando as seguintes restrições acadêmicas:

- Implementação manual da correlação (sem uso de funções prontas como `cv2.filter2D` ou `scipy.signal`)
- Processamento canal por canal (RGB)
- Máscaras configuráveis via arquivos JSON
- Suporte à dilatação do kernel (`r`)
- Suporte a `stride`
- Pós-processamento específico para operadores Sobel
- Operação **sem uso de padding**

---

# Conceito Teórico

## Correlação Espacial

A correlação espacial consiste na aplicação de uma máscara (kernel) sobre uma imagem.

\[
g(x,y) = \sum_{i,j} f(x+i, y+j) \cdot h(i,j)
\]

Onde:

- `f` → imagem de entrada  
- `h` → kernel (máscara)  
- `g` → imagem resultante  

---

## Correlação Dilatada (À Trous)

\[
g(x,y) = \sum_{i,j} f(x + r \cdot i, y + r \cdot j) \cdot h(i,j)
\]

O parâmetro `r` controla a **dilatação do kernel**, aumentando o campo receptivo sem alterar o tamanho da máscara.

---

# Arquitetura do Sistema

O sistema foi dividido em três módulos principais.

### main.py

Responsável por:

- leitura dos argumentos da linha de comando
- carregamento da imagem
- leitura do arquivo de configuração JSON
- execução da correlação dilatada
- salvamento da imagem resultante
- exibição opcional do resultado

---

### atrous.py

Implementa o **algoritmo de correlação dilatada**, incluindo:

- aplicação do kernel
- suporte à dilatação (`r`)
- suporte a `stride`
- processamento separado dos canais RGB
- aplicação opcional de função de ativação

---

### utils.py

Contém funções auxiliares utilizadas no projeto:

- `histogram_stretch()` → normalização de intensidade
- `sobel_postprocess()` → pós-processamento aplicado aos operadores Sobel

---

# Estrutura do Projeto

```
PDI_TRABALHO_ATROUS/
│
├── main.py
├── atrous.py
├── utils.py
│
├── configs/
│   ├── gaussian_5x5.json
│   ├── box_1x10.json
│   ├── box_10x1.json
│   ├── box_10x10.json
│   ├── sobel_horizontal.json
│   └── sobel_vertical.json
│
├── Shapes.png
├── testpat.1k.color2.tif
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

### Sintaxe geral

```bash
python main.py -i <imagem> -c <config.json> -o <saida> --show
```

### Parâmetros

| Parâmetro | Descrição |
|--------|--------|
| `-i` | imagem de entrada |
| `-c` | arquivo JSON contendo o kernel |
| `-o` | nome da imagem de saída |
| `--show` | exibe a imagem original e o resultado |

---

# Testes Solicitados

### 1️ Gaussian 5x5

```bash
python main.py -i Shapes.png -c configs/gaussian_5x5.json -o saida_gauss.png --show
```

---

### 2️ Box 1x10 (suavização horizontal)

```bash
python main.py -i Shapes.png -c configs/box_1x10.json -o saida_box_1x10.png --show
```

---

### 3️ Box 10x1 (suavização vertical)

```bash
python main.py -i Shapes.png -c configs/box_10x1.json -o saida_box_10x1.png --show
```

---

### 4️ Box 10x10

```bash
python main.py -i testpat.1k.color2.tif -c configs/box_10x10.json -o saida_box_10x10.png --show
```

---

### 5️ Sobel Horizontal

```bash
python main.py -i Shapes.png -c configs/sobel_horizontal.json -o saida_sobel_h.png --show
```

---

### 6️ Sobel Vertical

```bash
python main.py -i Shapes.png -c configs/sobel_vertical.json -o saida_sobel_v.png --show
```

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

### Campos

| Campo | Função |
|------|------|
| `kernel` | matriz da máscara |
| `r` | fator de dilatação |
| `stride` | passo da janela |
| `activation` | função de ativação |
| `is_sobel` | ativa pós-processamento Sobel |

---

# Análise dos Resultados

Os resultados obtidos demonstram o comportamento esperado dos filtros aplicados.

- O parâmetro **r** aumenta o campo receptivo da operação de correlação.
- O **stride** altera a densidade de amostragem da imagem resultante.
- Filtros **Box** realizam suavização baseada em média uniforme da vizinhança.
- O filtro **Gaussian** realiza suavização preservando melhor as bordas da imagem.
- Operadores **Sobel** detectam bordas horizontais ou verticais através da aproximação do gradiente da imagem.

Para os filtros Sobel é aplicado um pós-processamento composto por:

- cálculo do **valor absoluto do gradiente**
- **normalização para o intervalo [0,255]**

---

  
