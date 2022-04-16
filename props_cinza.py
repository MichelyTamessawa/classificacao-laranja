import os
import csv
import sys
import numpy as np
from skimage import color, io
from skimage.feature import greycomatrix, greycoprops

# classes das laranjas
# boa 0
# casca grossa 1
# podre 2
# dano praga 3
# verde 4

def calcula_greycoprops(tipo_laranja, sigla_tipo, dir_tipo):
    dir_resultado = "greycoprops_cinza/" + tipo_laranja

    lista_props = ['contrast', 'dissimilarity', 'homogeneity', 'ASM', 'energy', 'correlation']

    if tipo_laranja == 'Boa':
        classe_laranja = 0
    elif tipo_laranja == 'Casca Grossa':
        classe_laranja = 1
    elif tipo_laranja == 'Dano Praga':
        classe_laranja = 2
    elif tipo_laranja == 'Podre':
        classe_laranja = 3
    elif tipo_laranja == 'Verde':
        classe_laranja = 4
    else:
        print("Erro: não existe esta classe de laranja")
        sys.exit()
    
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
        dir_resultado_pasta = dir_resultado + pasta + ".csv"
        file = open(dir_resultado_pasta, "w", newline='')
        header = ['class', 
            'contrast_0', 'contrast_45', 'contrast_90', 'contrast_135',
            'dissimilarity_0', 'dissimilarity_45', 'dissimilarity_90', 'dissimilarity_135',
            'homogeneity_0', 'homogeneity_45', 'homogeneity_90', 'homogeneity_135',
            'ASM_0', 'ASM_45', 'ASM_90', 'ASM_135',
            'energy_0', 'energy_45', 'energy_90', 'energy_135',
            'correlation_0', 'correlation_45', 'correlation_90', 'correlation_135']

        writer = csv.writer(file)
        writer.writerow(header)
        
        # calculo do graycoprops de cada imagem
        for img in path_imagens:
            resultados = []
            img_cinza = color.rgb2gray(io.imread(img))
            img_cinza = np.uint(img_cinza * 255)
            glcm = greycomatrix(img_cinza, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256)

            # cálculo de cada propriedade
            for prop in lista_props:
                resultados.append(greycoprops(glcm, prop)[0,0])
                resultados.append(greycoprops(glcm, prop)[0,1])
                resultados.append(greycoprops(glcm, prop)[0,2])
                resultados.append(greycoprops(glcm, prop)[0,3])

            # escreve os resultados no arquivo
            writer.writerow([classe_laranja] + resultados)

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
