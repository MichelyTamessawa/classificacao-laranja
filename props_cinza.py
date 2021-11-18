import os
import numpy as np
from skimage import color, io
from skimage.feature import greycomatrix, greycoprops


# retorna listas contendo caminho + nome das imgs das laranjas para cada classe
def lista_nomes_imgs():
    laranjas_boas = []
    laranjas_casca_grossa = []
    laranjas_praga = []
    laranjas_podre = []
    laranjas_verde = []

    # diretorio atual
    cwd = os.getcwd()
    
    # diretório de cada classe
    path_boa = cwd + "/" + "Fold 7/Boa"
    path_casca_grossa =  cwd + "/" + "Fold 7/Ruin/Casca Grossa"
    path_praga =  cwd + "/" + "Fold 7/Ruin/Dano Praga"
    path_podre = cwd + "/" + "Fold 7/Ruin/Podre"
    path_verde = cwd + "/" + "Fold 7/Ruin/Verde"

    # obter o caminho de arquivo das imgs de laranjas boas
    for i in range(1, 11):
        path = path_boa + "/Fold " + str(i) + "B"
        nome_imgs = os.listdir(path)
        laranjas_boas += list(map(lambda x: path + "/" + x, nome_imgs))

    # laranjas Ruins
    classes_ruins = {
        "C": path_casca_grossa,
        "D": path_praga,
        "P": path_podre,
        "V": path_verde
    }

    # obter o caminho de arquivo das imgs de laranjas ruins
    for key, value in classes_ruins.items():
        for i in range(1, 11):
            path = value + "/Fold " + str(i) + str(key)
            nome_imgs = os.listdir(path)
            if key == "C": 
                laranjas_casca_grossa += list(map(lambda x: path + "/" + x, nome_imgs))
            elif key == "D": 
                laranjas_praga += list(map(lambda x: path + "/" + x, nome_imgs))
            elif key == "P": 
                laranjas_podre += list(map(lambda x: path + "/" + x, nome_imgs))
            elif key == "V": 
                laranjas_verde += list(map(lambda x: path + "/" + x, nome_imgs))
            else:
                print("Erro na leitura do nome dos arquivos das laranjas ruins")

    return laranjas_boas, laranjas_casca_grossa, laranjas_praga, laranjas_podre, laranjas_verde


# armazena as propriedades de textura extraidas do glcm em um arquivo
def calcula_props(lista_nomes_imgs, nome_arquivo):
    file = open(nome_arquivo, "w")

    # lista de propriedades da textura interessantes
    lista_props = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation']
    
    resultados = []

    for img in lista_nomes_imgs:
        img_cinza = color.rgb2gray(io.imread(img))
        img_cinza = np.uint(img_cinza * 255)
        
        glcm = greycomatrix(img_cinza, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256)
        
        # cálculo de cada propriedade
        for prop in lista_props:
            resultados.append(greycoprops(glcm, prop)[0,0])

        # escreve no arquivo os resultados da img
        file.write(str(resultados) + '\n')

    file.close


def main():
    imgs_entrada = lista_nomes_imgs()
    
    dir_resultados = ["greycoprops_cinza/boas.txt","greycoprops_cinza/casca_grossa.txt","greycoprops_cinza/praga.txt","greycoprops_cinza/podre.txt","greycoprops_cinza/verde.txt"]

    # cálculo as propriedades de textura a partir do glcm
    for i in range(0, 5):
        calcula_props(imgs_entrada[i], dir_resultados[i])

if __name__ == "__main__":
    main()
