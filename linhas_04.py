import cv2
import numpy as np

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)

gray = cv2.cvtColor(lane_image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
canny = cv2.Canny(blur, 50, 150)
# Aplica o detector de bordas de Canny à imagem suavizada (blur).
# A função cv2.Canny() detecta bordas na imagem ao identificar áreas onde há uma mudança abrupta de intensidade de pixels.
# Os parâmetros 50 e 150 representam os thresholds (limiares) mínimo e máximo, respectivamente. 
# Pixels com um gradiente de intensidade entre esses valores serão considerados bordas.


cv2.imshow('result', canny)
cv2.waitKey(0)