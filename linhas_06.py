import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    # Obtém a altura da imagem, que será usada para definir a base do polígono de interesse.
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
        ])
    # Define um polígono triangular que representa a região da estrada onde as faixas são esperadas.
    # Este polígono tem sua base na parte inferior da imagem e aponta para cima, imitando a forma de uma estrada à frente.
    mask = np.zeros_like(image)
    # Cria uma máscara preta (ou seja, todos os pixels têm valor zero) do mesmo tamanho da imagem original.
    cv2.fillPoly(mask, polygons, 255)
    # Preenche o polígono na máscara com branco (valor 255). 
    # Isso cria uma região de interesse onde a imagem será mantida, e o restante será descartado.
    return mask
    # Retorna a imagem mascarada, onde apenas a região de interesse é visível.

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = canny(lane_image)
cv2.imshow('result', region_of_interest(canny))
cv2.waitKey(0)