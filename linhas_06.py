import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    # Obtém a altura da imagem, que será usada para definir a região de interesse.
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
        ])
    # Define um polígono em formato de triângulo, que representa a área de interesse onde as linhas da pista geralmente estão localizadas.
    # Este polígono é formado por três pontos: dois na base da imagem (esquerda e direita) e um no centro superior.
    mask = np.zeros_like(image)
    # Cria uma máscara preta (toda preenchida com 0) do mesmo tamanho da imagem.
    cv2.fillPoly(mask, polygons, 255)
    # Preenche a área definida pelo polígono na máscara com branco (255), criando uma região de interesse.
    return mask
    # Retorna a máscara com a região de interesse definida. Esta máscara será utilizada para focar o processamento apenas na área relevante da imagem.

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = canny(lane_image)
cv2.imshow('result', region_of_interest(canny))
cv2.waitKey(0)