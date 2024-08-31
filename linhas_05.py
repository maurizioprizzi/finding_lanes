import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny
    # Define uma função `canny` que encapsula o processo de conversão para escala de cinza, suavização e detecção de bordas.
    # Isso torna o código mais modular e fácil de reutilizar para diferentes imagens.

def region_of_interest(image):
    height = image.shape[0]
    # Obtém a altura da imagem, que será usada para definir a região de interesse.
    
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
        ])
    # Define um polígono em formato de triângulo, que representa a área de interesse onde as linhas da pista geralmente estão localizadas.
    # Este polígono é formado por três pontos: dois na base da imagem (esquerda e direita) e um no centro superior.
    
    mask = np.zeros_like(image)
    # Cria uma máscara preta (toda preenchida com 0) do mesmo tamanho da imagem.

    cv2.fillPoly(mask, polygons, 255)
    # Preenche a área definida pelo polígono na máscara com branco (255), criando uma região de interesse.

    return mask
    # Retorna a máscara com a região de interesse definida. Esta máscara será utilizada para focar o processamento apenas na área relevante da imagem.

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)

canny = canny(lane_image)
# Aplica a função `canny` à imagem da pista para detectar bordas.

cv2.imshow('result', region_of_interest(canny))
# Aplica a máscara da região de interesse à imagem processada pelo Canny e exibe o resultado.

cv2.waitKey(0)
# Mantém a janela de visualização aberta até que uma tecla seja pressionada.