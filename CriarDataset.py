import numpy as np #fornece suporte para arrays multidimensionais eficientes, bem como funções matemáticas e operações de alto desempenho 
import pandas as pd # oferece suporte para análise de dados (manipulação, limpeza e visualização de dados tabulares) .

# Gerar dados aleatórios para os atributos
num_records = 1000
preco = np.random.uniform(1, 100, num_records)
volume = np.random.randint(1000, 10000, num_records)
indicador1 = np.random.randn(num_records)
indicador2 = np.random.randn(num_records)
sentimento = np.random.choice([-1, 1], num_records)
token_id = np.arange(num_records) + 1  # Atributo TokenId sequencial

# Gerar classe baseada em regras simuladas
classe = np.where(preco + volume * indicador1 + indicador2 + sentimento > 500, 1, 0)

# Criar DataFrame com os atributos e a classe
dataset = pd.DataFrame({
    'TokenId': token_id,
    'preco': preco,
    'volume': volume,
    'indicador1': indicador1,
    'indicador2': indicador2,
    'sentimento': sentimento,
    'classe': classe
})

# Salvar o dataset em um arquivo CSV
dataset.to_csv('dataset.csv', index=False)

