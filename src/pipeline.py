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


def aplicar_otsu(imagem_suavizada):
    """Cria uma mascara binaria usando um limiar calculado pelo Otsu."""
    _, mascara = cv2.threshold(
        imagem_suavizada,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )
    return mascara


def aplicar_morfologia(mascara, tamanho_kernel: int = 3):
    """Remove pontos isolados e fecha pequenas falhas na mascara."""
    if tamanho_kernel <= 0 or tamanho_kernel % 2 == 0:
        raise ValueError("O tamanho do kernel deve ser positivo e impar.")

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (tamanho_kernel, tamanho_kernel),
    )
    abertura = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    return cv2.morphologyEx(abertura, cv2.MORPH_CLOSE, kernel)


def detectar_bordas(
    imagem_suavizada,
    mascara_refinada,
    limiar_inferior: int = 50,
    limiar_superior: int = 150,
):
    """Combina os detalhes da imagem com o contorno da mascara."""
    if not 0 <= limiar_inferior < limiar_superior <= 255:
        raise ValueError("Os limiares do Canny sao invalidos.")

    bordas_detalhes = cv2.Canny(
        imagem_suavizada,
        limiar_inferior,
        limiar_superior,
    )
    bordas_estrutura = cv2.Canny(
        mascara_refinada,
        limiar_inferior,
        limiar_superior,
    )
    return cv2.bitwise_or(bordas_detalhes, bordas_estrutura)


def redimensionar(imagem, tamanho: int = 256):
    """Padroniza a imagem final no tamanho escolhido."""
    if tamanho <= 0:
        raise ValueError("O tamanho final deve ser positivo.")
    return cv2.resize(
        imagem,
        (tamanho, tamanho),
        interpolation=cv2.INTER_NEAREST,
    )
