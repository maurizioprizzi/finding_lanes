import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    # Cria uma nova imagem (toda preta) do mesmo tamanho que a imagem original, onde as linhas detectadas serão desenhadas.
    if lines is not None:
        # Verifica se alguma linha foi detectada pelo algoritmo de Hough.
        for line in lines:
            # Itera sobre cada linha detectada.
            x1, y1, x2, y2 = line.reshape(4)
            # Descompacta as coordenadas da linha (pontos de início e fim) que foram detectadas.
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            # Desenha a linha na imagem preta usando as coordenadas (x1, y1) e (x2, y2).
            # A cor da linha é azul (255, 0, 0) e a espessura é de 10 pixels.
    return line_image
    # Retorna a imagem com as linhas desenhadas.

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = canny(lane_image)
cropped_image = region_of_interest(canny)
lines = cv2.HoughLinesP(cropped_image, 2, (np.pi / 180), 100, np.array([]), minLineLength=40, maxLineGap=5)
# Aplica a Transformada de Hough probabilística para detectar linhas na imagem de bordas.
# O primeiro parâmetro é a imagem processada, o segundo é a resolução do acumulador da Transformada de Hough (em pixels), e o terceiro é a resolução angular (em radianos).
# O quarto parâmetro é o threshold que define o número mínimo de interseções para detectar uma linha.
# 'minLineLength' é o comprimento mínimo que uma linha precisa ter para ser considerada, e 'maxLineGap' é a distância máxima entre segmentos de linha para que sejam considerados uma única linha.
line_image = display_lines(lane_image, lines)
# Cria uma imagem com as linhas detectadas desenhadas sobre um fundo preto.
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# Combina a imagem original com as linhas desenhadas usando uma ponderação (80% da imagem original e 100% das linhas).
# Isso sobrepõe as linhas detectadas na imagem original, permitindo ver tanto as faixas da estrada quanto a imagem real.

cv2.imshow('result', combo_image)
cv2.waitKey(0)