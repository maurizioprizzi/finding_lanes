import cv2
# Importa a biblioteca OpenCV, que é essencial para a manipulação de imagens e vídeos em Python.

image = cv2.imread('test_image.jpg')
# Usa a função cv2.imread() para carregar a imagem 'test_image.jpg' do disco e armazena o resultado na variável 'image'.
# A imagem é carregada como um array multidimensional do NumPy, onde cada elemento representa um pixel da imagem.

cv2.imshow('result', image)
# Exibe a imagem carregada em uma janela. A função cv2.imshow() cria uma janela com o título 'result' e mostra a imagem armazenada em 'image'.

cv2.waitKey(0)
# A função cv2.waitKey(0) faz com que o programa espere até que uma tecla seja pressionada antes de fechar a janela.
# Isso é necessário para manter a janela aberta, caso contrário, ela fecharia imediatamente após ser exibida.
