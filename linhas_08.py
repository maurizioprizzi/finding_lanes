import cv2
# Importa a biblioteca OpenCV, que fornece funções para processamento de imagens e vídeos.

import numpy as np
# Importa a biblioteca NumPy, essencial para manipulação de arrays, que são usados para representar imagens e coordenadas.

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Converte a imagem original colorida para escala de cinza para simplificar o processamento.

    blur = cv2.GaussianBlur(gray, (5,5), 0)
    # Aplica um filtro Gaussiano para suavizar a imagem, reduzindo o ruído e detalhes finos que poderiam interferir na detecção de bordas.

    canny = cv2.Canny(blur, 50, 150)
    # Aplica o algoritmo de Canny para detectar bordas na imagem suavizada. 
    # Os parâmetros 50 e 150 são os thresholds (limiares) mínimo e máximo, controlando quais gradientes de intensidade são considerados bordas.

    return canny
    # Retorna a imagem resultante com as bordas detectadas.

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

image = cv2.imread('test_image.jpg')
# Carrega a imagem de um arquivo ('test_image.jpg') para começar o processamento.

lane_image = np.copy(image)
# Cria uma cópia da imagem original para preservar a imagem original inalterada.

canny = canny(lane_image)
# Aplica a função 'canny' à imagem copiada para detectar bordas.

cropped_image = region_of_interest(canny)
# Aplica a função 'region_of_interest' à imagem de bordas para isolar a área da estrada.

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
# Exibe a imagem final combinada, mostrando a estrada com as linhas das faixas destacadas.

cv2.waitKey(0)
# Mantém a janela de exibição aberta até que uma tecla seja pressionada.
