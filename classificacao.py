import sys
from os import path
import numpy as np
from skimage import color, io
from skimage.color.colorconv import rgb2hsv
from skimage.feature import greycomatrix, greycoprops
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn import svm

# boa 0
# casca grossa 1
# podre 2
# dano praga 3
# verde 4

classes_laranjas = ["Boa", "Casca Grossa", "Dano Praga", "Podre", "Verde"]
siglas = ["B", "C", "D", "P", "V"]

def leitura_cinza():
    # leitura dos arquivos com as propriedades extraidas

    X = []
    
    for index, tipo in enumerate(classes_laranjas):
        for i in range(1, 11):
            path_resultado = "greycoprops_cinza/" + tipo + "/Fold " + str(i) + siglas[index] + ".txt"

            try:
                file = open(path_resultado, "r")
            except FileNotFoundError:
                print("Arquivo não encontrado")
            
            lines = file.readlines()
            
            data = [list(map (float, x.strip().split())) for x in lines]            
            
            X += data

    Y = [0]*2270 + [1]*2270 + [2]*2220 + [3]*2270 + [4]*2270

    return X, Y


def leitura_colorida():
     # leitura dos arquivos com as propriedades extraidas

    X = []
    
    for index, tipo in enumerate(classes_laranjas):
        for i in range(1, 11):
            path_resultado = "greycoprops_colorida/" + tipo + "/Fold " + str(i) + siglas[index] + ".txt"

            try:
                file = open(path_resultado, "r")
            except FileNotFoundError:
                print("Arquivo não encontrado")
            
            lines = file.readlines()
            
            data = [list(map (float, x.strip().split())) for x in lines]            
            
            X += data

    Y = [0]*2270 + [1]*2270 + [2]*2220 + [3]*2270 + [4]*2270

    return X, Y


def validacao_cruzada_knn(X, Y, k):

    clf = KNeighborsClassifier(n_neighbors=k)

    scores = cross_val_score(clf, X, Y, cv=10, scoring='accuracy')

    print("Média dos resultados com knn k = {}: {}".format(k, scores.mean()))
    

def validacao_cruzada_svm(X, Y):
    
    clf = svm.SVC(gamma='auto')

    scores = cross_val_score(clf, X, Y, cv=10, scoring='accuracy')

    print("Média dos resultados com SVM: {}".format(scores.mean()))


def main(tipo_leitura):
    if tipo_leitura == "rgb":
        X, Y = leitura_colorida()
    else:
        X, Y = leitura_cinza()

    validacao_cruzada_knn(X, Y, 3)
    validacao_cruzada_knn(X, Y, 5)
    validacao_cruzada_knn(X, Y, 7)

    validacao_cruzada_svm(X, Y)

if __name__ == "__main__":
    main(sys.argv[1])