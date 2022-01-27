import sys
import numpy as np
from os import path
from sklearn import svm
from skimage import color, io
from skimage.color.colorconv import rgb2hsv
from skimage.feature import greycomatrix, greycoprops
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score


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

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,random_state=100)

    return x_train, x_test, y_train, y_test


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

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3,random_state=100)

    return x_train, x_test, y_train, y_test


def validacao_cruzada_knn(X, Y, k):

    knn = KNeighborsClassifier(n_neighbors=k)

    scores = cross_val_score(knn, X, Y, cv=10, scoring='accuracy')

    print("Média dos resultados com knn k = {}: {}".format(k, scores.mean()))
    

def validacao_cruzada_svm(X, Y):
    
    knn = svm.SVC(gamma='auto')

    scores = cross_val_score(knn, X, Y, cv=10, scoring='accuracy')

    print("Média dos resultados com SVM: {}".format(scores.mean()))


def validacao_gridsearchcv(X, Y):
    knn = KNeighborsClassifier()

    k_range = list(range(1, 31))
    
    param_grid = dict(n_neighbors=k_range)

    grid = GridSearchCV(knn, param_grid, cv=10, scoring='accuracy', return_train_score=False,verbose=1)

    grid_search=grid.fit(X, Y)

    k_result = grid_search.best_params_['n_neighbors'] 
    
    print(grid_search.best_params_)

    accuracy = grid_search.best_score_ *100
    
    print("Accuracy for our training dataset with tuning is : {:.2f}%".format(accuracy) )

    return k_result


def verificacao_acuracia(x_train, x_test, y_train, y_test, k):
    knn = KNeighborsClassifier(n_neighbors=k)

    knn.fit(x_train, y_train)

    y_test_result = knn.predict(x_test) 

    test_accuracy = accuracy_score(y_test, y_test_result)*100

    print("Accuracy for our testing dataset with tuning is : {:.2f}%".format(test_accuracy) )


def main(tipo_leitura):
    if tipo_leitura == "rgb":
        x_train, x_test, y_train, y_test = leitura_colorida()
    else:
        x_train, x_test, y_train, y_test = leitura_cinza()

    # validacao_cruzada_knn(X, Y, 3)
    # validacao_cruzada_knn(X, Y, 5)
    # validacao_cruzada_knn(X, Y, 7)
    # validacao_cruzada_svm(X, Y)

    # testando varios parametros de k com gridsearch
    k = validacao_gridsearchcv(x_train, y_train)
    verificacao_acuracia(x_train, x_test, y_train, y_test, k)

if __name__ == "__main__":
    main(sys.argv[1])