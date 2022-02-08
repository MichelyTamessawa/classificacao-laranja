import sys
import numpy as np
import pandas as pd
from os import path
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import SelectKBest, chi2

# boa 0
# casca grossa 1
# podre 2
# dano praga 3
# verde 4

classes_laranjas = ["Boa", "Casca Grossa", "Dano Praga", "Podre", "Verde"]
siglas = ["B", "C", "D", "P", "V"]

def leitura_cinza():
    # leitura dos arquivos com as propriedades extraidas

    x = []
    
    for index, tipo in enumerate(classes_laranjas):
        for i in range(1, 11):
            path_resultado = "greycoprops_cinza/" + tipo + "/Fold " + str(i) + siglas[index] + ".csv"

            try:
                data = pd.read_csv(path_resultado)

            except FileNotFoundError:
                print("Arquivo não encontrado")
                        
            x.append(data)
    
    X = pd.concat(x, axis=0, ignore_index=True)

    Y = [0]*2270 + [1]*2270 + [2]*2220 + [3]*2270 + [4]*2270

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2,random_state=42)

    return x_train, x_test, y_train, y_test


def leitura_colorida():
    # leitura dos arquivos com as propriedades extraidas

    x = []
    
    for index, tipo in enumerate(classes_laranjas):
        for i in range(1, 11):
            path_resultado = "greycoprops_colorida/" + tipo + "/Fold " + str(i) + siglas[index] + ".csv"

            try:
                data = pd.read_csv(path_resultado)
            except FileNotFoundError:
                print("Arquivo não encontrado")
                                    
            x.append(data)

    X = pd.concat(x, axis=0, ignore_index=True)

    Y = [0]*2270 + [1]*2270 + [2]*2220 + [3]*2270 + [4]*2270

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2,random_state=42)

    return x_train, x_test, y_train, y_test


def validacao_cruzada_knn(X, Y, k):
    knn = KNeighborsClassifier(n_neighbors=k)

    scores = cross_val_score(knn, X, Y, cv=10, scoring='accuracy')

    print("Média dos resultados com knn k = {}: {}".format(k, scores.mean()))
    

def validacao_cruzada_svm(X, Y):
    clf = svm.SVC(gamma='auto')

    scores = cross_val_score(clf, X, Y, cv=10, scoring='accuracy')

    print("Média dos resultados com SVM: {}".format(scores.mean()))


def validacao_gridsearchcv(x_train, x_test, y_train, y_test):
    knn = KNeighborsClassifier()
    
    """ parameters = {
        'n_neighbors': [1,3,5,7,9,11],
        'leaf_size': (20,40,1),
        'p': (1,2),
        'weights': ('uniform', 'distance'),
        'metric': ('minkowski', 'chebyshev') } """

    parameters = {
        'n_neighbors': [1,3,5,7,9,11]}

    grid = GridSearchCV(estimator=knn, param_grid=parameters, cv=10, scoring='accuracy')

    grid_search = grid.fit(x_train, y_train)
    
    print(grid_search.best_params_)

    accuracy = grid_search.best_score_ *100    
    print("Accuracy for our training dataset with tuning is : {:.2f}%".format(accuracy))

    y_test_result = grid.predict(x_test)
    test_accuracy = accuracy_score(y_test, y_test_result)*100
    print("Accuracy for our testing dataset with tuning is : {:.2f}%".format(test_accuracy))


def selecao_caracteristicas(X, Y):
    melhores_caracteristicas = SelectKBest(score_func=chi2, k=3)
    
    fit = melhores_caracteristicas.fit(X, Y)

    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(X.columns)

    featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    featureScores.columns = ['Specs','Score']
    result_columns = featureScores.nlargest(6,'Score')

    print("Melhores caracteristicas extraídas:")
    print(result_columns)

    return result_columns['Specs'].tolist()


def gridsearchcv_melhores_caracteristicas(X, Y, colunas):
    X = X[colunas]

    knn = KNeighborsClassifier()

    k_range = list(range(1, 31))
    
    param_grid = dict(n_neighbors=k_range)

    grid = GridSearchCV(knn, param_grid, cv=10, scoring='accuracy', return_train_score=False,verbose=1)

    grid_search = grid.fit(X, Y)

    k_result = grid_search.best_params_['n_neighbors'] 
    
    print(grid_search.best_params_)

    accuracy = grid_search.best_score_ *100
    
    print("Accuracy for our training dataset with tuning is : {:.2f}%".format(accuracy) )

    return k_result
    
    
def main():
    print("Tons de Cinza")
    x_train, x_test, y_train, y_test = leitura_cinza()
    k = validacao_gridsearchcv(x_train, x_test, y_train, y_test)

    print("RGB")
    x_train, x_test, y_train, y_test = leitura_colorida()
    k = validacao_gridsearchcv(x_train, x_test, y_train, y_test)

    #validacao_gridsearchcv(x_train, y_train)
    #verificacao_acuracia(x_train, x_test, y_train, y_test, 1)
    # validacao_cruzada_knn(X, Y, 5)
    # validacao_cruzada_knn(X, Y, 7)
    # validacao_cruzada_svm(X, Y)

    # testando varios parametros de k com gridsearch
    # k = validacao_gridsearchcv(x_train, y_train)
    # verificacao_acuracia(x_train, x_test, y_train, y_test, k)

    # selecao das melhores caracteristicas
    # colunas = selecao_caracteristicas(x_train, y_train)
    # validacao_gridsearchcv(x_train, y_train)

    # melhores caracteristicas imagens rgb
    # colunas = selecao_caracteristicas(x_train, y_train)
    # gridsearchcv_melhores_caracteristicas(x_train, y_train, colunas)

if __name__ == "__main__":
    main()