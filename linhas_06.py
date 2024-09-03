import cv2
# Importa a biblioteca OpenCV, que contém funções para processamento de imagens e vídeos.

import numpy as np
# Importa a biblioteca NumPy, que é usada para manipulação de arrays, essencial para operações com imagens.

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Converte a imagem original de cores (BGR) para escala de cinza. 
    # Isso simplifica a imagem, facilitando a detecção de bordas, pois a cor não é mais um fator.

    blur = cv2.GaussianBlur(gray, (5,5), 0)
    # Aplica um filtro Gaussiano para suavizar a imagem. 
    # Isso ajuda a reduzir o ruído e os detalhes finos, que podem interferir na detecção de bordas.

    canny = cv2.Canny(blur, 50, 150)
    # Aplica o algoritmo de Canny para detecção de bordas. 
    # O Canny identifica áreas na imagem onde há uma mudança abrupta de intensidade, que normalmente representam bordas.
    # Os parâmetros 50 e 150 são os thresholds (limiares) mínimo e máximo para a detecção de bordas.

    return canny
    # Retorna a imagem resultante após a aplicação do detector de bordas de Canny.

def region_of_interest(image):
    height = image.shape[0]
    # Obtém a altura da imagem, que será usada para definir a base do polígono de interesse.

    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    # Define um polígono triangular que representa a região da estrada onde as faixas são esperadas.
    # Este polígono tem sua base na parte inferior da imagem e aponta para cima, imitando a forma de uma estrada à frente.

    mask = np.zeros_like(image)
    # Cria uma máscara preta (ou seja, todos os pixels têm valor zero) do mesmo tamanho da imagem original.

    cv2.fillPoly(mask, polygons, 255)
    # Preenche o polígono na máscara com branco (valor 255). 
    # Isso cria uma região de interesse onde a imagem será mantida, e o restante será descartado.

    masked_image = cv2.bitwise_and(image, mask)
    # Aplica a máscara à imagem usando a operação bitwise AND. 
    # Isso faz com que apenas a área dentro do polígono (região de interesse) seja mantida, 
    # enquanto o resto da imagem é escurecido (preto).

    return masked_image
    # Retorna a imagem mascarada, onde apenas a região de interesse é visível.

image = cv2.imread('test_image.jpg')
# Carrega a imagem de um arquivo ('test_image.jpg') para começar o processamento.

lane_image = np.copy(image)
# Cria uma cópia da imagem original para preservar a versão original inalterada durante o processamento.

canny = canny(lane_image)
# Aplica a função 'canny' à imagem copiada para detectar as bordas na imagem.

cropped_image = region_of_interest(canny)
# Aplica a função 'region_of_interest' à imagem resultante da detecção de bordas.
# Isso isola a área onde as faixas da estrada são esperadas, descartando o restante da imagem.

cv2.imshow('result', cropped_image)
# Exibe a imagem final, que mostra apenas a região de interesse com as bordas detectadas.

cv2.waitKey(0)
# Mantém a janela de exibição aberta até que uma tecla seja pressionada.
