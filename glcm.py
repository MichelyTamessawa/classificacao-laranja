import os
import numpy as np
from skimage import color, io
from skimage.feature import greycomatrix
from skimage.util import img_as_uint

# Leitura das imagens
laranjasBoas = []
laranjasCascaGrossa = []
laranjasPraga = []
laranjasPodre = []
laranjasVerde = []

pathBoa = "Fold 7\Boa"
pathCascaGrossa = "Fold 7\Ruin\Casca Grossa"
pathPraga = "Fold 7\Ruin\Dano Praga"
pathPodre = "Fold 7\Ruin\Podre"
pathVerde = "Fold 7\Ruin\Verde"

# Laranjas Boas
for i in range(1, 11):
    path = pathBoa + "\Fold " + str(i) + "B"
    nomeImagens = os.listdir(path)
    laranjasBoas += list(map(lambda x: path + "\\" + x, nomeImagens))

print("{} laranjas boas".format(len(laranjasBoas)))

# Laranjas Ruins
ClassesRuins = {"C": pathCascaGrossa,
                "D": pathPraga,
                "P": pathPodre,
                "V": pathVerde}

for key, value in ClassesRuins.items():
    for i in range(1, 11):
        path = value + "\Fold " + str(i) + str(key)
        nomeImagens = os.listdir(path)

        if key == "C": 
            laranjasCascaGrossa += list(map(lambda x: path + "\\" + x, nomeImagens))
        elif key == "D": 
            laranjasPraga += list(map(lambda x: path + "\\" + x, nomeImagens))
        elif key == "P": 
            laranjasPodre += list(map(lambda x: path + "\\" + x, nomeImagens))
        elif key == "V": 
            laranjasVerde += list(map(lambda x: path + "\\" + x, nomeImagens))
        else:
            print("Erro na leitura do nome dos arquivos das laranjas ruins")

print("{} laranjas ruins".format(len(laranjasCascaGrossa)+len(laranjasVerde)+len(laranjasPodre)+len(laranjasPraga)))

# Transformar as imagens em tons de cinza
GLCMLaranjasBoas = []
GLCMLaranjasCascaGrossa = []
GLCMLaranjasPraga = []
GLCMLaranjasPodre = []
GLCMLaranjasVerde = []

for image in laranjasBoas:
    img = color.rgb2gray(io.imread(image))
    img = np.uint(img * 255)
    glcm = greycomatrix(img, distances=[1], angles=[
                        0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
    GLCMLaranjasBoas.append(glcm)

print("{} glcm laranjas boas".format(len(GLCMLaranjasBoas)))

# for image in laranjasCascaGrossa:
#     img = color.rgb2gray(io.imread(image))
#     img = np.uint(img * 255)
#     glcm = greycomatrix(img, distances=[1], angles=[
#                         0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
#     GLCMLaranjasCascaGrossa.append(glcm)

# for image in laranjasPraga:
#     img = color.rgb2gray(io.imread(image))
#     img = np.uint(img * 255)
#     glcm = greycomatrix(img, distances=[1], angles=[
#                         0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
#     GLCMLaranjasPraga.append(glcm)

# for image in laranjasPodre:
#     img = color.rgb2gray(io.imread(image))
#     img = np.uint(img * 255)
#     glcm = greycomatrix(img, distances=[1], angles=[
#                         0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
#     GLCMLaranjasPodre.append(glcm)

# for image in laranjasVerde:
#     img = color.rgb2gray(io.imread(image))
#     img = np.uint(img * 255)
#     glcm = greycomatrix(img, distances=[1], angles=[
#                         0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
#     GLCMLaranjasVerde.append(glcm)


# io.imshow(img)
# io.show()

# to do
# ler todas as imagens da base de dados

# passar para tons de cinza
# calcular 1 glcm para cada laranja

# deixar a imagem colorida e calcular 3 glcm para cada laranja
