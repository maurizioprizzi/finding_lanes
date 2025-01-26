import cv2

# Carrega a imagem
image = cv2.imread('test_image.jpg')

# Exibe a imagem
cv2.imshow('result', image)

# Aguarda uma tecla ser pressionada
cv2.waitKey(0)

# Fecha todas as janelas abertas
cv2.destroyAllWindows()