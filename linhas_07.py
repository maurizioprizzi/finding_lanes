import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    # Aplica a máscara à imagem usando a operação bitwise AND. 
    # Isso faz com que apenas a área dentro do polígono (região de interesse) seja mantida, 
    # enquanto o resto da imagem é escurecido (preto).
    return masked_image

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = canny(lane_image)
cropped_image = region_of_interest(canny)
# Aplica a função 'region_of_interest' à imagem resultante da detecção de bordas.
# Isso isola a área onde as faixas da estrada são esperadas, descartando o restante da imagem.
cv2.imshow('result', cropped_image)
# Exibe a imagem final, que mostra apenas a região de interesse com as bordas detectadas.
cv2.waitKey(0)