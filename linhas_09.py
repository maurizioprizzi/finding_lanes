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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Converte a imagem original colorida para escala de cinza, simplificando o processamento e a detecção de bordas.

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Aplica um filtro Gaussiano para suavizar a imagem, reduzindo o ruído que poderia interferir na detecção de bordas.

    canny = cv2.Canny(blur, 50, 150)
    # Aplica o detector de bordas de Canny para identificar as bordas na imagem suavizada.

    return canny
    # Retorna a imagem com as bordas detectadas.

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    # Cria uma nova imagem preta (com zeros) do mesmo tamanho que a imagem original, onde as linhas detectadas serão desenhadas.

    if lines is not None:
        # Verifica se alguma linha foi detectada.

        for x1, y1, x2, y2 in lines:
            # Itera sobre cada linha detectada e descompacta as coordenadas dos pontos iniciais e finais.

            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
            # Desenha a linha na imagem preta com a cor azul (255, 0, 0) e espessura de 10 pixels.

    return line_image
    # Retorna a imagem com as linhas desenhadas.

def region_of_interest(image):
    height = image.shape[0]
    # Obtém a altura da imagem para ajudar a definir a região de interesse.

    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    # Define um polígono triangular que cobre a área da estrada onde as faixas são esperadas.
    # O polígono é definido por três pontos: dois na base (à esquerda e à direita) e um no topo (centro superior).

    mask = np.zeros_like(image)
    # Cria uma máscara preta (zeros) do mesmo tamanho da imagem original.

    cv2.fillPoly(mask, polygons, 255)
    # Preenche o polígono na máscara com branco (255), definindo a área de interesse.

    masked_image = cv2.bitwise_and(image, mask)
    # Aplica a máscara à imagem, mantendo apenas a área dentro do polígono e escurecendo o resto.

    return masked_image
    # Retorna a imagem mascarada, onde apenas a região de interesse é visível.

# image = cv2.imread('test_image.jpg')
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 2, (np.pi / 180), 100, np.array([]), minLineLength=40, maxLineGap=5)
# averaged_lines = average_slope_intercept(lane_image, lines)
# line_image = display_lines(lane_image, averaged_lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# cv2.imshow('result', combo_image)
# cv2.waitKey(0)

cap = cv2.VideoCapture('test2.mp4')
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, (np.pi / 180), 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow('result', combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()