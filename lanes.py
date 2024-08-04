# Esta linha importa a biblioteca OpenCV, que é uma das bibliotecas mais utilizadas para processamento de imagens e visão computacional.
# Ela fornece ferramentas para leitura e manipulação de imagens, bem como para aplicar transformações e filtros.
import cv2

#NumPy é uma biblioteca para manipulação de arrays e matrizes multidimensionais em Python.
# É usada em conjunto com o OpenCV porque as imagens são tratadas como arrays, e NumPy fornece funcionalidades eficientes para manipulação desses dados.
import numpy as np

# Esta função lê uma imagem do arquivo especificado ('test_image.jpg') e a carrega como um array NumPy.
# O OpenCV representa imagens como arrays multidimensionais, onde cada elemento representa um pixel na imagem, com valores para as cores BGR (azul, verde, vermelho).
image = cv2.imread('test_image.jpg')

# Faz uma cópia do array da imagem original. Isso é importante para garantir que o processamento ou manipulação subsequente não afete a imagem original.
# Trabalhar com uma cópia permite testar diferentes transformações sem alterar os dados originais.
lane_image = np.copy(image)

#  Converte a imagem de cor para escala de cinza. A conversão para escala de cinza é um passo comum em processamento de imagens porque simplifica a análise, reduzindo a quantidade de dados de cor, o que pode melhorar o desempenho e a eficiência de muitos algoritmos de detecção, como bordas ou objetos.
gray = cv2.cvtColor(lane_image, cv2.COLOR_BGR2GRAY)

# Aplica um filtro Gaussiano para suavizar a imagem. O filtro Gaussiano reduz o ruído e os detalhes na imagem, o que é útil para preparar a imagem para a detecção de bordas. O parâmetro (5, 5) especifica o tamanho do kernel, e 0 é o desvio padrão, que controla o grau de suavização.
blur = cv2.GaussianBlur(gray, (5, 5), 0) # 5*5 kernel, deviation of 0

# Aplica o detector de bordas Canny. Este algoritmo é usado para detectar bordas na imagem, identificando regiões de rápido contraste. Os parâmetros 50 e 150 são os limites inferior e superior para a histerese no processo de detecção de bordas. Ajustar esses valores influencia a sensibilidade da detecção de bordas.
canny = cv2.Canny(blur, 50, 150)

cv2.imshow('result', canny)
cv2.waitKey(0)