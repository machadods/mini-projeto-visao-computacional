# Pré-processamento de imagens de peças metálicas

Mini-projeto de visão computacional desenvolvido em Python com a biblioteca OpenCV.

## Objetivo

O objetivo é preparar imagens de peças metálicas para uso futuro em um modelo de Machine Learning. O programa não classifica as peças. Ele realiza transformações que reduzem ruídos, separam regiões da imagem e destacam contornos e possíveis falhas.

## Dataset

Foi utilizado o dataset [Casting Product Image Data for Quality Inspection](https://drive.google.com/file/d/1K5gNxQ7RXA-nb4boNzPYQTJlRvJyYBD1/view?usp=sharing), indicado no enunciado.

As imagens foram organizadas da seguinte forma:

```text
data/raw/
├── def_front/    # 781 imagens com defeito
└── ok_front/     # 519 imagens sem defeito
```

O dataset e os resultados não são enviados ao GitHub.

## Estrutura

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── image_io.py
│   ├── main.py
│   └── pipeline.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Preparação do ambiente

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as bibliotecas:

```powershell
pip install -r requirements.txt
```

Depois, coloque as pastas `def_front` e `ok_front` dentro de `data/raw`.

## Execução

Na raiz do projeto, execute:

```powershell
python -m src.main --input data/raw --output data/processed
```

O programa procura todas as imagens nas subpastas de entrada e mantém a separação entre `def_front` e `ok_front` na pasta de saída.

## Etapas do processamento

1. Conversão da imagem BGR para escala de cinza.
2. Aplicação de Gaussian Blur com kernel `5 x 5` para redução de ruído.
3. Limiarização automática pelo método de Otsu.
4. Abertura e fechamento morfológicos com kernel elíptico `3 x 3`.
5. Detecção de bordas com Canny usando limiares 50 e 150.
6. Redimensionamento da imagem final para `256 x 256` pixels.
7. Salvamento em PNG no diretório de saída.

As bordas da imagem suavizada são combinadas com as bordas da máscara refinada. Isso ajuda a preservar detalhes internos e o contorno principal da peça.

## Resultado

O processamento foi executado nas 1.300 imagens do dataset:

| Categoria | Quantidade |
|---|---:|
| `def_front` | 781 |
| `ok_front` | 519 |
| Total | 1.300 |

Todas as imagens foram processadas sem falhas e salvas com tamanho `256 x 256` pixels.

## Versionamento

O projeto utiliza a branch `main` para a versão estável e a branch `development` durante o desenvolvimento. Os commits foram separados conforme as funcionalidades implementadas.
