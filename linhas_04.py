import cv2
import numpy as np

# Lê a imagem do arquivo
image = cv2.imread('test_image.jpg')

# Cria uma cópia da imagem original para preservar os dados da imagem original
lane_image = np.copy(image)

# Converte a imagem copiada para escala de cinza
# A escala de cinza é útil para simplificar o processamento, pois reduz a imagem a um único canal (intensidade)
gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)

# Aplica um desfoque gaussiano na imagem em escala de cinza
# O desfoque é usado para suavizar a imagem, reduzindo o ruído e facilitando o processamento de bordas
# (5, 5) é o tamanho do kernel de desfoque, e 0 é o desvio padrão da distribuição Gaussiana
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Aplica o detector de bordas Canny à imagem borrada
# Canny é um algoritmo usado para detectar bordas na imagem
# Os parâmetros 50 e 150 definem os limites inferior e superior para a detecção de bordas
canny = cv2.Canny(blur, 50, 150)

# Exibe a imagem processada com o detector de bordas em uma janela chamada 'result'
cv2.imshow('result', canny)

# Aguarda até que qualquer tecla seja pressionada para continuar
cv2.waitKey(0)

# Fecha todas as janelas abertas criadas por OpenCV
cv2.destroyAllWindows()