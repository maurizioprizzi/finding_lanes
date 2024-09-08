import cv2
import numpy as np

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)

gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
# Aplica um filtro Gaussiano à imagem em escala de cinza usando a função cv2.GaussianBlur().
# O filtro Gaussiano suaviza a imagem, reduzindo o ruído e os detalhes finos. Isso é feito ao calcular uma média ponderada dos pixels em torno de cada pixel, utilizando uma matriz 5x5 (o primeiro argumento).
# O terceiro argumento é o desvio padrão da distribuição Gaussiana. Um valor de 0 faz com que o OpenCV o calcule automaticamente com base no tamanho do kernel.

cv2.imshow('result', blur)
cv2.waitKey(0)