import os
import numpy as np
from skimage import color, io
from skimage.feature import greycomatrix

def leituraImagens():
    # listas contendo caminho + nome das imagens das laranjas para cada classe
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

    # laranjas boas
    for i in range(1, 11):
        path = pathBoa + "\Fold " + str(i) + "B"
        nomeImagens = os.listdir(path)
        laranjasBoas += list(map(lambda x: path + "\\" + x, nomeImagens))

    # laranjas Ruins
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

    return laranjasBoas, laranjasCascaGrossa, laranjasPraga, laranjasPodre, laranjasVerde

def transformacaoTonsCinza(lista_nome_imagens):
    lista_glcm = []
    

    for imagem in lista_nome_imagens:
        imagem_cinza = color.rgb2gray(io.imread(imagem))
        imagem_cinza = np.uint(imagem_cinza * 255)
        glcm = greycomatrix(imagem_cinza, distances=[1], angles=[
                            0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
        lista_glcm.append(glcm)

    return lista_glcm

    
def main():
    laranjasBoas, laranjasCascaGrossa, laranjasPraga, laranjasPodre, laranjasVerde = leituraImagens()
    glcm_boas = transformacaoTonsCinza(laranjasBoas)
    glcm_casca_grossa = transformacaoTonsCinza(laranjasCascaGrossa)
    glcm_praga = transformacaoTonsCinza(laranjasPraga)
    glcm_podre = transformacaoTonsCinza(laranjasPodre)
    glcm_verde = transformacaoTonsCinza(laranjasVerde)

if __== "__main__":
    main()
    
# to do
# ler todas as imagens da base de dados

# passar para tons de cinza
# calcular 1 glcm para cada laranja

# deixar a imagem colorida e calcular 3 glcm para cada laranja
