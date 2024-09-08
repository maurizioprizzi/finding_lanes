import cv2
# Importa a biblioteca OpenCV, usada para processamento de imagens e vídeos.

import numpy as np
# Importa a biblioteca NumPy, usada para operações matemáticas e manipulação de arrays.

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    # Descompacta os parâmetros da linha, que são a inclinação (slope) e a interseção (intercept) com o eixo y.

    y1 = image.shape[0]
    # Define a coordenada y1 como a altura da imagem (a base da imagem).

    y2 = int(y1 * (3 / 5))
    # Define y2 como um ponto mais acima na imagem, correspondente a 3/5 da altura total da imagem.
    # Isso define o comprimento da linha que será desenhada, garantindo que ela não se estenda até o topo da imagem.

    x1 = int((y1 - intercept) / slope)
    # Calcula a coordenada x1 correspondente a y1 usando a equação da linha (y = mx + b, rearranjada como x = (y - b) / m).

    x2 = int((y2 - intercept) / slope)
    # Calcula a coordenada x2 correspondente a y2 da mesma forma.

    return np.array([x1, y1, x2, y2])
    # Retorna as coordenadas calculadas como um array NumPy, representando a linha a ser desenhada.

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    # Inicializa duas listas para armazenar os parâmetros das linhas (inclinação e interceptação) que pertencem ao lado esquerdo e direito da pista.

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        # Descompacta as coordenadas x e y dos dois pontos que definem cada linha.

        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        # Calcula os parâmetros da linha (inclinação e interceptação) usando uma regressão linear (ajuste polinomial de grau 1) entre os pontos x e y.

        slope = parameters[0]
        intercept = parameters[1]
        # Atribui a inclinação e a interceptação com o eixo y.

        if slope < 0:
            left_fit.append((slope, intercept))
            # Se a inclinação for negativa, a linha é adicionada à lista de linhas à esquerda da pista.
        else:
            right_fit.append((slope, intercept))
            # Se a inclinação for positiva, a linha é adicionada à lista de linhas à direita da pista.

    left_fit_average = np.average(left_fit, axis=0)
    # Calcula a média dos parâmetros (inclinação e interceptação) para todas as linhas à esquerda, resultando em uma linha média representativa.

    right_fit_average = np.average(right_fit, axis=0)
    # Faz o mesmo para as linhas à direita.

    left_line = make_coordinates(image, left_fit_average)
    # Gera as coordenadas da linha média à esquerda usando os parâmetros médios calculados.

    right_line = make_coordinates(image, right_fit_average)
    # Gera as coordenadas da linha média à direita da mesma forma.

    return np.array([left_line, right_line])
    # Retorna um array contendo as coordenadas das linhas à esquerda e à direita da pista.

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny_image = canny(lane_image)
cropped_image = region_of_interest(canny_image)
lines = cv2.HoughLinesP(cropped_image, 2, (np.pi / 180), 100, np.array([]), minLineLength=40, maxLineGap=5)
averaged_lines = average_slope_intercept(lane_image, lines)
# Calcula as médias das inclinações e interceptações das linhas detectadas à esquerda e à direita, gerando linhas representativas para cada lado da pista.
line_image = display_lines(lane_image, averaged_lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)

cv2.imshow('result', combo_image)
cv2.waitKey(0)