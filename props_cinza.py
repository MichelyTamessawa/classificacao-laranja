import os
import numpy as np
from skimage import color, io
from skimage.feature import greycomatrix, greycoprops

lista_props = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation']

def calcula_greycoprops(tipo_laranja, sigla_tipo, dir_tipo):
    dir_resultado = "greycoprops_cinza/" + tipo_laranja
    
    # cria os diretorios dos resultados
    try:
        os.mkdir("greycoprops_cinza")
        print("O diretório greycoprops_cinza foi criado")
    except FileExistsError:
        print("O diretório greycoprops_cinza já existe")

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
            resultados = []
            img_cinza = color.rgb2gray(io.imread(img))
            img_cinza = np.uint(img_cinza * 255)
            glcm = greycomatrix(img_cinza, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256)

            # cálculo de cada propriedade
            for prop in lista_props:
                resultados.append(greycoprops(glcm, prop)[0,0])

            # escreve os resultados no arquivo
            for x in resultados:
                file.write(str(x) + " ")
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
