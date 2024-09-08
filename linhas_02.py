import cv2
import numpy as np
# Importa a biblioteca NumPy, que é utilizada para manipulação de arrays, essencial para operações eficientes em imagens e outras estruturas de dados numéricos.

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
# Cria uma cópia da imagem original usando a função np.copy(). 
# Isso permite que a imagem original permaneça inalterada, enquanto as operações de processamento são realizadas na cópia.

gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
# Converte a imagem copiada de colorida (BGR) para tons de cinza usando a função cv2.cvtColor().
# A conversão para tons de cinza simplifica a imagem, reduzindo o número de canais de cor de 3 (BGR) para 1, o que facilita o processamento em etapas futuras.

cv2.imshow('result', gray)
cv2.waitKey(0)