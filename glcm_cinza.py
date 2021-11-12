import os
import numpy as np
from skimage import color, io
from skimage.feature import greycomatrix


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

    print("{} laranjas boas".format(len(laranjas_boas)))

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

    print("{} laranjas ruins".format(len(laranjas_casca_grossa)+len(laranjas_verde)+len(laranjas_podre)+len(laranjas_praga)))

    return laranjas_boas, laranjas_casca_grossa, laranjas_praga, laranjas_podre, laranjas_verde


def calcula_glcm(lista_nome_imagens):
    lista_glcm = []
    
    for imagem in lista_nome_imagens:
        imagem_cinza = color.rgb2gray(io.imread(imagem))
        print(imagem_cinza.dtype)
        imagem_cinza = np.uint(imagem_cinza * 255)
        glcm = greycomatrix(imagem_cinza, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256, symmetric=True, normed=True)
        lista_glcm.append(glcm)

    print("{} glcms".format(len(lista_glcm)))

    return lista_glcm


def grava_arquivo(nome_arquivo, lista):
    arquivo = open(nome_arquivo,'w')
    
    for elemento in lista:
        arquivo.write("%s\n" % elemento)
        
    arquivo.close()


def main():
    laranjas_boas, laranjas_casca_grossa, laranjas_praga, laranjas_podre, laranjas_verde = lista_nomes_imagens()
    glcm_boas = calcula_glcm(laranjas_boas)
    #grava_arquivo("glcm_boas.txt", glcm_boas)

    """ glcm_casca_grossa = calcula_glcm(laranjasCascaGrossa)
    glcm_praga = calcula_glcm(laranjasPraga)
    glcm_podre = calcula_glcm(laranjasPodre)
    glcm_verde = calcula_glcm(laranjasVerde) """


if __name__ == "__main__":
    main()
