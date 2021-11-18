import os
import numpy as np
from skimage import io
from skimage.feature import greycomatrix , greycoprops


# retorna listas contendo caminho + nome das imagens das laranjas para cada classe
def lista_nomes_imgs():
    laranjas_boas = []
    laranjas_casca_grossa = []
    laranjas_praga = []
    laranjas_podre = []
    laranjas_verde = []

    # diretorio atual
    cwd = os.getcwd()
    
    # diretório de cada classe
    dir_boa = cwd + "/" + "Fold 7/Boa"
    dir_casca_grossa =  cwd + "/" + "Fold 7/Ruin/Casca Grossa"
    dir_praga =  cwd + "/" + "Fold 7/Ruin/Dano Praga"
    dir_podre = cwd + "/" + "Fold 7/Ruin/Podre"
    dir_verde = cwd + "/" + "Fold 7/Ruin/Verde"

    # obter o caminho de arquivo das imagens de laranjas boas
    for i in range(1, 11):
        dir = dir_boa + "/Fold " + str(i) + "B"
        nome_imgs = os.listdir(dir)
        laranjas_boas += list(map(lambda x: dir + "/" + x, nome_imgs))

    # laranjas Ruins
    classes_ruins = {"C": dir_casca_grossa,
                    "D": dir_praga,
                    "P": dir_podre,
                    "V": dir_verde}

    # obter o caminho de arquivo das imagens de laranjas ruins
    for key, value in classes_ruins.items():
        for i in range(1, 11):
            dir = value + "/Fold " + str(i) + str(key)
            nome_imgs = os.listdir(dir)

            if key == "C": 
                laranjas_casca_grossa += list(map(lambda x: dir + "/" + x, nome_imgs))
            elif key == "D": 
                laranjas_praga += list(map(lambda x: dir + "/" + x, nome_imgs))
            elif key == "P": 
                laranjas_podre += list(map(lambda x: dir + "/" + x, nome_imgs))
            elif key == "V": 
                laranjas_verde += list(map(lambda x: dir + "/" + x, nome_imgs))
            else:
                print("Erro na leitura do nome dos arquivos das laranjas ruins")

    return laranjas_boas, laranjas_casca_grossa, laranjas_praga, laranjas_podre, laranjas_verde


# armazena as propriedades extraidas do glcm em um arquivo
def calcula_props(lista_nomes_imgs, nome_arquivo):
    file = open(nome_arquivo, "w")
    
    for nome_img in lista_nomes_imgs:
        img_colorida = io.imread(nome_img)

        # separação a img nas 3 bandas RGB
        img_r = img_colorida[:,:,0]
        img_g = img_colorida[:,:,1]
        img_b = img_colorida[:,:,2]

        # cálculo do glcm de cada banda
        glcm_r = greycomatrix(img_r, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4])
        glcm_g = greycomatrix(img_g, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4])
        glcm_b = greycomatrix(img_b, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4])
        
        # cálculo das propriedades para cada glcm
        x_r = calcula_props_RGB(glcm_r)
        x_g = calcula_props_RGB(glcm_g)
        x_b = calcula_props_RGB(glcm_b)

        # resultado das propriedades de textura nas 3 bandas
        x = [x_r, x_g, x_b]

        file.write(str(x) + '\n')

    file.close


# cálculo as propriedades de textura pelo glcm em cada banda do RGB
def calcula_props_RGB(glcm):
    # lista de propriedades da textura interessantes
    lista_props = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation']
    
    resultados = []

    # cálculo de cada propriedade
    for prop in lista_props:
        resultados.append(greycoprops(glcm, prop)[0,0])

    return resultados

def main():
    imgs_entrada = lista_nomes_imgs()

    # diretório para armazenar os resultados
    dir_resultados = ["greycoprops_colorido/boas.txt","greycoprops_colorido/casca_grossa.txt","greycoprops_colorido/praga.txt","greycoprops_colorido/podre.txt","greycoprops_colorido/verde.txt"]

    # cálculo das propriedades de textura a partir do glcm
    for i in range(0, 5):
        calcula_props(imgs_entrada[i], dir_resultados[i])

if __name__ == "__main__":
    main()
    