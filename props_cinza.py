import os
import numpy as np
from skimage import color, io
from skimage.feature import greycomatrix, greycoprops


def lista_nomes_imagens():
    # listas contendo caminho + nome das imagens das laranjas para cada classe
    laranjas_boas = []
    laranjas_casca_grossa = []
    laranjas_praga = []
    laranjas_podre = []
    laranjas_verde = []

    # diretorio atual
    cwd = os.getcwd()
    
    path_boa = cwd + "/" + "Fold 7/Boa"
    path_casca_grossa =  cwd + "/" + "Fold 7/Ruin/Casca Grossa"
    path_praga =  cwd + "/" + "Fold 7/Ruin/Dano Praga"
    path_podre = cwd + "/" + "Fold 7/Ruin/Podre"
    path_verde = cwd + "/" + "Fold 7/Ruin/Verde"

    # laranjas boas
    for i in range(1, 11):
        path = path_boa + "/Fold " + str(i) + "B"
        nome_imagens = os.listdir(path)
        laranjas_boas += list(map(lambda x: path + "/" + x, nome_imagens))

    # laranjas Ruins
    classes_ruins = {"C": path_casca_grossa,
                    "D": path_praga,
                    "P": path_podre,
                    "V": path_verde}

    for key, value in classes_ruins.items():
        for i in range(1, 11):
            path = value + "/Fold " + str(i) + str(key)
            nome_imagens = os.listdir(path)
            if key == "C": 
                laranjas_casca_grossa += list(map(lambda x: path + "/" + x, nome_imagens))
            elif key == "D": 
                laranjas_praga += list(map(lambda x: path + "/" + x, nome_imagens))
            elif key == "P": 
                laranjas_podre += list(map(lambda x: path + "/" + x, nome_imagens))
            elif key == "V": 
                laranjas_verde += list(map(lambda x: path + "/" + x, nome_imagens))
            else:
                print("Erro na leitura do nome dos arquivos das laranjas ruins")

    return laranjas_boas, laranjas_casca_grossa, laranjas_praga, laranjas_podre, laranjas_verde


def calcula_props(lista_nome_imagens, nome_arquivo):
    # armazena as propriedades de textura extraidas do glcm em um arquivo
    file = open(nome_arquivo, "w")
    
    for imagem in lista_nome_imagens:
        imagem_cinza = color.rgb2gray(io.imread(imagem))
        imagem_cinza = np.uint(imagem_cinza * 255)
        
        glcm = greycomatrix(imagem_cinza, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256)
        
        contrast = greycoprops(glcm, 'contrast')[0,0]
        dissimilarity = greycoprops(glcm, 'dissimilarity')[0,0]
        homogeneity = greycoprops(glcm, 'homogeneity')[0,0]
        ASM = greycoprops(glcm, 'ASM')[0,0]
        energy = greycoprops(glcm, 'energy')[0,0]
        correlation = greycoprops(glcm, 'correlation')[0,0]

        x = [contrast, dissimilarity, homogeneity, ASM, energy, correlation]

        file.write(str(x) + '\n')

    file.close


def armazena_props():
    laranjas_boas, laranjas_casca_grossa, laranjas_praga, laranjas_podre, laranjas_verde = lista_nomes_imagens()

    # calcula as propriedades de textura a partir do glcm
    calcula_props(laranjas_boas, "greycoprops_cinza/" + "boas.txt")
    calcula_props(laranjas_casca_grossa, "greycoprops_cinza/" + "casca_grossa.txt")
    calcula_props(laranjas_praga, "greycoprops_cinza/" + "praga.txt")
    calcula_props(laranjas_podre, "greycoprops_cinza/" + "podre.txt")
    calcula_props(laranjas_verde, "greycoprops_cinza/" + "verde.txt")


def main():
    armazena_props()

if __name__ == "__main__":
    main()
