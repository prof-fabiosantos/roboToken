from web3 import Web3 # biblioteca Python que permite interagir com uma rede Ethereum ou BSC
import json # oferece suporte para trabalhar com dados no formato JSON
from datetime import datetime, timedelta # fornece classes e funções para trabalhar com datas e horários
import time #  oferece funções relacionadas ao tempo, como medir intervalos de tempo,
import aiohttp # é uma biblioteca Python usada para realizar requisições HTTP assíncronas
import asyncio # oferece suporte para programação assíncrona em Python.
import joblib # oferece suporte para carregamento do modelo de machine learning.

# Configure a conexão Web3 com a BSC Testnet (por exemplo, usando o provedor do Infura)
w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
if w3.isConnected():
    print("O Bot está conectado:")
else:
    print("O Bot não está conectado:")

chain_id = 97  # BSC Testnet

# Endereço e ABI do contrato de roteamento da PancakeSwap na BSC Testnet
pancakeswap_router_address = '0xD99D1c33F9fC3444f8101754aBC46c52416550D1'
contract_abi = json.loads('[{   "inputs": [     {       "internalType": "uint256",       "name": "amountIn",       "type": "uint256"     },     {       "internalType": "uint256",       "name": "amountOutMin",       "type": "uint256"     },     {       "internalType": "address[]",       "name": "path",       "type": "address[]"     },     {       "internalType": "address",       "name": "to",       "type": "address"     },     {       "internalType": "uint256",       "name": "deadline",       "type": "uint256"     }   ],   "name": "swapExactTokensForTokens",   "outputs": [     {       "internalType": "uint256[]",       "name": "amounts",       "type": "uint256[]"     }   ],   "stateMutability": "nonpayable",   "type": "function" }]')

# Chaves endereço e privada da conta do usuário BSC Testnet - Metamask
account = "0x2c24d0B31583912a9461FC95DFc200B53bca4e6A"
private_key = 'c58517d6dfc740985bb51e0293c6d5dce4ddbfa730edd097ca70d3e877e8b21e'

# Criar o contrato de roteamento da PancakeSwap
pancakeswap_router_contract = w3.eth.contract(address=pancakeswap_router_address, abi=contract_abi)

# Função para trocar tokens usando o contrato de roteamento da PancakeSwap
def swap_tokens(token_in, token_out, amount_in):
    # Definir os parâmetros da função swapExactTokensForTokens
    amount_in = Web3.toWei(amount_in, 'ether')  # Quantidade de tokens de entrada (por exemplo, 1 token)
    amount_out_min = 0  # Quantidade mínima de tokens de saída aceita (ajuste conforme necessário)
    path = [Web3.toChecksumAddress(token_in), Web3.toChecksumAddress(token_out)]  # Caminho da troca de token A para token B
    to = account  # Endereço que receberá os tokens de saída (em formato de endereço checksum)
  
    # Obter o timestamp atual em milissegundos
    timestamp_atual = int(datetime.now().timestamp() * 1000)
    # Adicionar 10000 milissegundos ao timestamp atual
    deadline = timestamp_atual + 10000

    # Construir a transação
    transaction = pancakeswap_router_contract.functions.swapExactTokensForTokens(
        amount_in,
        amount_out_min,
        path,
        to,
        deadline
    ).buildTransaction({
        'chainId': chain_id,
        'gas': 2000000,  # Limite de gás para a transação (ajuste conforme necessário)
        'gasPrice': w3.toWei('50', 'gwei'),  # Preço do gás (ajuste conforme necessário)
        'nonce': w3.eth.getTransactionCount(account),  # Em letras minúsculas
    })

    # Assinar a transação
    signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
    # Enviar a transação assinada
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return tx_hash.hex()

# Função para aprovar que o contrado de roteamento da PancakeSwap possa transferir tokens da conta do usuário
def approve_spending(token_address, spender_address, amount):
         
    # ABI do contrato do token WBNB na BSC Testnet
    contract_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]')
    # Carregando o contrato do token
    token_contract = w3.eth.contract(address=token_address, abi=contract_abi)

    # Converter o valor para o formato esperado pelo contrato (em wei)
    amount_in_wei = w3.toWei(amount, 'ether')
    nonce = w3.eth.getTransactionCount(account)

    # Construir a transação de aprovação
    transaction = token_contract.functions.approve(spender_address, amount_in_wei).buildTransaction({
        'chainId': chain_id,
        'gas': 200000,  # Limite de gás para a transação (ajuste conforme necessário)
        'gasPrice': w3.toWei('100', 'gwei'),  # Preço do gás (ajuste conforme necessário)
        'nonce': nonce + 1,
    })

    # Assinar a transação
    signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
    # Enviar a transação assinada
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    return tx_hash.hex()

# Carregar o modelo treinado
model = joblib.load('modelo.pkl')

async def predict(TokenId, preco, volume, indicador1, indicador2, sentimento):    

    new_data = [[TokenId, preco, volume, indicador1, indicador2, sentimento]]  # Novos dados para previsão com TokenId 1001
    prediction = model.predict(new_data)   
                 
    return prediction

# Predição para compra de Token
PREDiCTION = [1] # 1 = Vai valorizar 

async def main():
    stop_order = False  # Variável para controlar a ordem de parada do robô

    print("Olá sou o Robô Vendedor de Token, para interromper o bot pressione ao mesmo tempo CTRL + C")
    time.sleep(5)  

    while not stop_order:        
        try:
            
            TokenId = 1000
            preco = 100
            volume = 2000
            indicador1 = 0.75
            indicador2 = 0.9
            sentimento = 1 
            
            """
            TokenId = 999
            preco = 94.40234153384169
            volume = 7994
            indicador1 = -0.07712893927465866
            indicador2 = -0.22530859547228227
            sentimento = 1
            """
            
            response = await predict(TokenId, preco, volume, indicador1, indicador2, sentimento)            
            
            if response == [1]:
                print("Resultado da previsão: Vai valorizar!")
            elif response == [0]:
                print("Resultado da previsão: Vai desvalorizar.")
        
        except Exception as e:
            print("Error:", str(e))
        
        if response == PREDiCTION:
            # Vender tokens se o preço estiver acima ou igual ao limiar de venda
            print("De acordo com previsão da IA o token vai valorizar ")
            print("Portanto, vou comprar token")

            # Exemplo de uso para trocar WBNB por CAKE na BSC Testnet

            # Endereço do contrato do token WBNB
            token_in_address = '0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd' 
            # Endereço do contrato do token CAKE
            token_out_address = '0x8d008B313C1d6C7fE2982F62d32Da7507cF43551' 
            amount_in_tokens = 0.001  # Quantidade de tokens de entrada (por exemplo, 0.001 WBNB)

            transaction1_hash = approve_spending(token_in_address, pancakeswap_router_address, amount_in_tokens)
            print("Aprove executado. Hash da transação:", transaction1_hash)
            time.sleep(30) 
            transaction2_hash = swap_tokens(token_in_address, token_out_address, amount_in_tokens)
            print("Compra executada. Hash da transação:", transaction2_hash)
        
        else:
            print("Não irei comprar porque de acordo com a IA o token vai desvalorizar")

        # Aguardar um tempo antes de verificar novamente o preço
        time.sleep(20)  # Substitua pelo intervalo desejado em segundos


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())








