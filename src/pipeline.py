import cv2


def converter_para_cinza(imagem):
    """Converte a imagem colorida do OpenCV para escala de cinza."""
    if imagem is None or imagem.ndim != 3:
        raise ValueError("A conversao precisa receber uma imagem colorida.")
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def reduzir_ruido(imagem_cinza, tamanho_kernel: int = 5):
    """Aplica Gaussian Blur antes das etapas de segmentacao."""
    if tamanho_kernel <= 0 or tamanho_kernel % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser positivo e impar.")
    return cv2.GaussianBlur(
        imagem_cinza,
        (tamanho_kernel, tamanho_kernel),
        0,
    )
