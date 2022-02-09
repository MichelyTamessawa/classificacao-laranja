import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

# classificação das laranjas
# boa 0
# casca grossa 1
# podre 2
# dano praga 3
# verde 4

# leitura dos arquivos com as propriedades extraidas
def leitura(dir):
    siglas_laranjas = ["B", "C", "D", "P", "V"]
    classes_laranjas = ["Boa", "Casca Grossa", "Dano Praga", "Podre", "Verde"]
    
    dados = []
    
    for index, tipo in enumerate(classes_laranjas):
        for i in range(1, 11):
            path_resultado = dir + tipo + "/Fold " + str(i) + siglas_laranjas[index] + ".csv"

            try:
                linha = pd.read_csv(path_resultado)

            except FileNotFoundError:
                print("Arquivo não encontrado")
                        
            dados.append(linha)
    
    df = pd.concat(dados, axis=0, ignore_index=True) 
    
    X = df.drop('class', axis=1)

    y = df['class']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

    return x_train, x_test, y_train, y_test


def knn_grafico_acuracia(x_train, x_test, y_train, y_test, params):
    acuracia = []

    for i in range(1, 30):
        # treinamento com dados de treino
        if params:
            knn = KNeighborsClassifier(n_neighbors=i, leaf_size=params['leaf_size'], metric=params['metric'], p=params['p'], weights=params['weights'])
        else:
            knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(x_train, y_train)

        # verifica se o modelo erra na predição
        y_test_result = knn.predict(x_test)
        acuracia.append(accuracy_score(y_test, y_test_result)*100)

    # gráfico de linha
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, 30), acuracia, color='red', linestyle='dashed', marker='o', markerfacecolor='blue', markersize=10)
    plt.title('K-NN usando GridSearchCV: Acurácia x Valor de K')
    plt.xlabel('K')
    plt.ylabel('Acurácia')
    plt.show()


def knn_gridsearchcv(x_train, x_test, y_train, y_test):
    print("> K-NN com gridsearchcv")

    knn = KNeighborsClassifier()
    parameters = {
        'n_neighbors': range(1,30),
        'leaf_size': (20,40,1),
        'p': (1,2),
        'weights': ('uniform', 'distance'),
        'metric': ('minkowski', 'chebyshev') }

    # selecionando os melhores parâmetros para o modelo
    grid = GridSearchCV(estimator=knn, param_grid=parameters, cv=10, scoring='accuracy')
    grid_search = grid.fit(x_train, y_train)
    print("\tParâmetros: {}".format(grid_search.best_params_))

    # acurácia do modelo com os dados de treino
    accuracy = grid_search.best_score_ *100    
    print("\tAcurácia para os dados de treinamento: {:.2f}%".format(accuracy))

    # acurácia do modelo com os dados de teste
    y_test_result = grid.predict(x_test)
    test_accuracy = accuracy_score(y_test, y_test_result)*100
    print("\tAcurácia para os dados de teste:  {:.2f}%".format(test_accuracy))

    return grid_search.best_params_
    

def knn_params(x_train, x_test, y_train, y_test, params=None):
    print("> K-NN usando os melhores parâmetros dados pelo gridsearchcv")
    
    # treinamento com dados de treino
    knn = KNeighborsClassifier(n_neighbors=params['n_neighbors'], leaf_size=params['leaf_size'], metric=params['metric'], p=params['p'], weights=params['weights'])
    knn.fit(x_train, y_train)

    # acurácia com os dados de teste
    y_test_result = knn.predict(x_test)
    test_accuracy = accuracy_score(y_test, y_test_result)*100
    print("\tAcurácia do modelo: {:.2f}%".format(test_accuracy))

    # análise dos erros
    print("\nAnálise dos erros")
    print (pd.crosstab(y_test, y_test_result, rownames=['Real'], colnames=['Predito'], margins=True))


def main():
    print("======================Tons de Cinza======================")
    x_train, x_test, y_train, y_test = leitura("greycoprops_cinza/") 
    knn_grafico_acuracia(x_train, x_test, y_train, y_test, False)
    params = knn_gridsearchcv(x_train, x_test, y_train, y_test)
    knn_params(x_train, x_test, y_train, y_test, params)
    knn_grafico_acuracia(x_train, x_test, y_train, y_test, params)

    print("============================RGB==========================")
    x_train, x_test, y_train, y_test = leitura("greycoprops_cinza/") 
    knn_grafico_acuracia(x_train, x_test, y_train, y_test, False)
    params = knn_gridsearchcv(x_train, x_test, y_train, y_test)
    knn_params(x_train, x_test, y_train, y_test, params)
    knn_grafico_acuracia(x_train, x_test, y_train, y_test, params)


if __name__ == "__main__":
    main()