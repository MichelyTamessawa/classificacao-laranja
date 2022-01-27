import os
import numpy as np
from skimage import io
from skimage.feature import greycomatrix , greycoprops

lista_props = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation']

# cálculo as propriedades de textura pelo glcm em cada banda do RGB
def calcula_props_RGB(glcm):
    resultados = []

    # cálculo de cada propriedade
    for prop in lista_props:
        resultados.append(greycoprops(glcm, prop)[0,0])

    return resultados

def calcula_greycoprops(tipo_laranja, sigla_tipo, dir_tipo):
    dir_resultado = "greycoprops_colorida/" + tipo_laranja
    
    # cria os diretorios dos resultados
    try:
        os.mkdir("greycoprops_colorida")
        print("O diretório greycoprops_colorida foi criado")
    except FileExistsError:
        print("O diretório greycoprops_colorida já existe")

    try:
        os.mkdir(dir_resultado)
        print("O diretório {} foi criado".format(dir_resultado))
    except FileExistsError:
        print("O diretório {} já existe, então ele será reescrito".format(dir_resultado))

    for i in range(1, 11):
        path_imagens = []
        pasta = "/Fold " + str(i) + sigla_tipo

        # obtendo os nomes das imagens
        path = dir_tipo + pasta
        nome_imgs = os.listdir(path)
        path_imagens += list(map(lambda x: path + "/" + x, nome_imgs))
        
        # abre o arquivo para gravação dos resultados
        dir_resultado_pasta = dir_resultado + pasta + ".txt"
        file = open(dir_resultado_pasta, "w")

        # calculo do graycoprops de cada imagem
        for img in path_imagens:
            img_colorida = io.imread(img)

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

            # escreve no arquivo os resultados da img
            for resultados in x:
                [file.write(str(p) + " ") for p in resultados]
            file.write('\n')

        file.close
    
    
def main():
    cwd = os.getcwd()
    
    # diretório de cada classe
    path_boa = cwd + "/" + "Fold 7/Boa"
    path_casca_grossa =  cwd + "/" + "Fold 7/Ruin/Casca Grossa"
    path_praga =  cwd + "/" + "Fold 7/Ruin/Dano Praga"
    path_podre = cwd + "/" + "Fold 7/Ruin/Podre"
    path_verde = cwd + "/" + "Fold 7/Ruin/Verde"

    calcula_greycoprops("Boa", "B", path_boa)
    calcula_greycoprops("Casca Grossa", "C", path_casca_grossa)
    calcula_greycoprops("Dano Praga", "D", path_praga)
    calcula_greycoprops("Podre", "P", path_podre)
    calcula_greycoprops("Verde", "V", path_verde)


if __name__ == "__main__":
    main()
     