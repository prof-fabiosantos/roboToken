from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Carregar o modelo treinado
model = joblib.load('modelo.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Obter os dados do POST request
    data = request.get_json()
    
    # Extrair os atributos do JSON
    new_data = [
        data['TokenId'],
        data['preco'],
        data['volume'],
        data['indicador1'],
        data['indicador2'],
        data['sentimento']
    ]
    
    # Fazer a previsão com o modelo carregado
    prediction = model.predict([new_data])
    
    # Converter a previsão para um tipo JSON serializável
    prediction = prediction.item()
    
    # Retornar a previsão como JSON
    return jsonify({'prediction': prediction}), 200

if __name__ == '__main__':
    app.run()



