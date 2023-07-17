import pandas as pd # oferece suporte para análise de dados (manipulação, limpeza e visualização de dados tabulares) .
from sklearn.model_selection import train_test_split #é utilizada para dividir um conjunto de dados em conjuntos de treinamento e teste
from sklearn.linear_model import LogisticRegression # é usada para realizar a regressão logística, que é um algoritmo de aprendizado de máquina utilizado principalmente para problemas de classificação binária
import joblib # oferece suporte para salvar do modelo de machine learning.

# Carregamento do dataset
dataset = pd.read_csv("dataset.csv")

# Separar atributos e classe
X = dataset[['TokenId', 'preco', 'volume', 'indicador1', 'indicador2', 'sentimento']].values
y = dataset['classe'].values

# Divisão do dataset em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento do modelo
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Avaliação do modelo
accuracy = model.score(X_test, y_test)
print(f"Acurácia do modelo: {accuracy}")

# Salvando o modelo treinado
joblib.dump(model, 'modelo.pkl')

# Exemplo de carregamento e previsão com o modelo
loaded_model = joblib.load('modelo.pkl')
new_data = [[1001, 100, 2000, 0.75, 0.9, 1]]  # Novos dados para previsão com TokenId 1001
prediction = loaded_model.predict(new_data)
print(f"Previsão: {prediction}")
