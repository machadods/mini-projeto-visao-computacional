import argparse
from pathlib import Path

from src.image_io import (
    carregar_imagem,
    listar_imagens,
    montar_caminho_saida,
    salvar_imagem,
)
from src.pipeline import (
    aplicar_morfologia,
    aplicar_otsu,
    converter_para_cinza,
    detectar_bordas,
    redimensionar,
    reduzir_ruido,
)


def processar_imagem(caminho_imagem: Path):
    imagem = carregar_imagem(caminho_imagem)
    cinza = converter_para_cinza(imagem)
    suavizada = reduzir_ruido(cinza)
    mascara = aplicar_otsu(suavizada)
    mascara_refinada = aplicar_morfologia(mascara)
    bordas = detectar_bordas(suavizada, mascara_refinada)
    return redimensionar(bordas)


def main():
    parser = argparse.ArgumentParser(
        description="Pre-processamento de imagens de pecas metalicas"
    )
    parser.add_argument("--input", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    args = parser.parse_args()

    try:
        imagens = listar_imagens(args.input)
    except FileNotFoundError as erro:
        print(f"Erro: {erro}")
        return 1

    if not imagens:
        print("Nenhuma imagem encontrada.")
        return 1

    processadas = 0
    falhas = 0

    for indice, caminho in enumerate(imagens, start=1):
        try:
            resultado = processar_imagem(caminho)
            destino = montar_caminho_saida(caminho, args.input, args.output)
            salvar_imagem(destino, resultado)
            processadas += 1
        except (ValueError, OSError) as erro:
            falhas += 1
            print(f"Falha em {caminho.name}: {erro}")

        if indice % 100 == 0:
            print(f"Processadas {indice} de {len(imagens)} imagens")

    print("\nResumo")
    print(f"Imagens encontradas: {len(imagens)}")
    print(f"Processadas com sucesso: {processadas}")
    print(f"Falhas: {falhas}")
    print("Tamanho das imagens finais: 256 x 256")
    return 0 if processadas else 1


if __name__ == "__main__":
    raise SystemExit(main())
