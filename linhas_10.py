import cv2
import numpy as np

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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

cap = cv2.VideoCapture('test2.mp4')
# Abre o arquivo de vídeo 'test2.mp4'. O objeto 'cap' é usado para capturar os quadros do vídeo.

while(cap.isOpened()):
    # Um loop que continua enquanto o vídeo estiver aberto e os quadros puderem ser lidos.

    _, frame = cap.read()
    # Lê o próximo quadro do vídeo. A variável 'frame' contém a imagem do quadro atual.

    canny_image = canny(frame)
    # Aplica a função 'canny' à imagem do quadro, que realiza a detecção de bordas.

    cropped_image = region_of_interest(canny_image)
    # Aplica a função 'region_of_interest' para isolar a área de interesse da imagem, geralmente a região da estrada.

    lines = cv2.HoughLinesP(cropped_image, 2, (np.pi / 180), 100, np.array([]), minLineLength=40, maxLineGap=5)
    # Utiliza a Transformada de Hough probabilística para detectar linhas no espaço de bordas.
    # O segundo argumento é a resolução da distância (2 pixels) e o terceiro é a resolução angular (1 grau em radianos).
    # 'minLineLength' define o comprimento mínimo da linha, e 'maxLineGap' define a distância máxima entre segmentos de linha para que sejam considerados uma única linha.

    averaged_lines = average_slope_intercept(frame, lines)
    # Calcula as linhas médias para o lado esquerdo e direito da pista, com base nas linhas detectadas pela Transformada de Hough.
    # A média ajuda a suavizar o comportamento das linhas, eliminando ruídos.

    line_image = display_lines(frame, averaged_lines)
    # Cria uma nova imagem onde as linhas médias calculadas são desenhadas sobre um fundo preto.

    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    # Combina a imagem original do quadro com a imagem das linhas desenhadas.
    # Usa uma ponderação de 80% da imagem original e 100% da imagem das linhas, para que as faixas sejam claramente visíveis na imagem resultante.

    cv2.imshow('result', combo_image)
    # Exibe a imagem final, mostrando as faixas da estrada sobre a imagem original.

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Espera 1 milissegundo e verifica se a tecla 'q' foi pressionada.
    # Se for pressionada, o loop é interrompido e o vídeo para de ser processado.


cap.release()
cv2.destroyAllWindows()