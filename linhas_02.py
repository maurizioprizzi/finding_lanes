import cv2
import numpy as np

# Lê a imagem do arquivo
image = cv2.imread('test_image.jpg')

# Cria uma cópia da imagem original para preservar os dados da imagem original
lane_image = np.copy(image)

# Converte a imagem copiada para escala de cinza
gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)

# Exibe a imagem em escala de cinza em uma janela chamada "result"
cv2.imshow('result', gray)

# Aguarda até que qualquer tecla seja pressionada para continuar
cv2.waitKey(0)

# Fecha todas as janelas abertas criadas por OpenCV
cv2.destroyAllWindows()
