import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny
    # Define uma função `canny` que encapsula o processo de conversão para escala de cinza, suavização e detecção de bordas.
    # Isso torna o código mais modular e fácil de reutilizar para diferentes imagens.

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = canny(lane_image)
# Aplica a função `canny` à imagem da pista para detectar bordas.
plt.imshow(canny)
plt.show()