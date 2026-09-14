from pathlib import Path

import cv2


EXTENSOES_VALIDAS = {".jpg", ".jpeg", ".png", ".bmp"}


def listar_imagens(pasta_entrada: Path) -> list[Path]:
    """Retorna todas as imagens encontradas nas subpastas de entrada."""
    if not pasta_entrada.exists():
        raise FileNotFoundError(f"Pasta nao encontrada: {pasta_entrada}")

    return sorted(
        arquivo
        for arquivo in pasta_entrada.rglob("*")
        if arquivo.is_file() and arquivo.suffix.lower() in EXTENSOES_VALIDAS
    )


def carregar_imagem(caminho: Path):
    imagem = cv2.imread(str(caminho))
    if imagem is None:
        raise ValueError(f"Nao foi possivel abrir: {caminho}")
    return imagem


def montar_caminho_saida(
    caminho_imagem: Path,
    pasta_entrada: Path,
    pasta_saida: Path,
) -> Path:
    caminho_relativo = caminho_imagem.relative_to(pasta_entrada)
    return (pasta_saida / caminho_relativo).with_suffix(".png")


def salvar_imagem(caminho: Path, imagem) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(caminho), imagem):
        raise OSError(f"Nao foi possivel salvar: {caminho}")
