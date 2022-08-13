# Classificação de Imagens de Laranjas por Técnicas de Processamento Digital de Imagens e Reconhecimento de Padrões

Código-fonte do Trabalho de Conclusão de Curso apresentado ao Departamento de Informática do curso Ciência da Computação. Este trabalho utiliza técnicas de PDI para extração de características das imagens de laranjas pela matriz GLCM, que são as entradas de dados para os classificadores K-NN, RF e SVM.
Bibliotecas instaladas e utilizadas neste trabalho:
- NumPy
- Pandas
- Scikit-image
- Scikit-learn

## Como executar:

### Clone este repositório
$ git clone <https://github.com/MichelyTamessawa/classificacao-laranja.git>

### Acesse a pasta do projeto no terminal/cmd
$ cd classificacao-laranja

### Execute o código da extração das propriedades 
$ python3 props_cinza.py

$ python3 props_colorido.py

### Execute o código da classificação no colab 
Alterar o caminho dos diretórios que armazem os dados das propriedades do GLCM
