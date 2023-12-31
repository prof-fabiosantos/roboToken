from web3 import Web3
import json
from datetime import datetime, timedelta
import time

# Configure a conexão Web3 com a BSC Testnet (por exemplo, usando o provedor do Infura)
w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
print("O Bot está conectado:", w3.isConnected())
chain_id = 97  # BSC Testnet

# Endereço do contrato de roteamento da PancakeSwap na BSC Testnet
pancakeswap_router_address = '0xD99D1c33F9fC3444f8101754aBC46c52416550D1'
contract_abi = json.loads('[{   "inputs": [     {       "internalType": "uint256",       "name": "amountIn",       "type": "uint256"     },     {       "internalType": "uint256",       "name": "amountOutMin",       "type": "uint256"     },     {       "internalType": "address[]",       "name": "path",       "type": "address[]"     },     {       "internalType": "address",       "name": "to",       "type": "address"     },     {       "internalType": "uint256",       "name": "deadline",       "type": "uint256"     }   ],   "name": "swapExactTokensForTokens",   "outputs": [     {       "internalType": "uint256[]",       "name": "amounts",       "type": "uint256[]"     }   ],   "stateMutability": "nonpayable",   "type": "function" }]')

# Chaves privadas e endereços BSC Testnet
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


def approve_spending(token_address, spender_address, amount):
    w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
       
    # Carregando o contrato do token
    contract_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]')
    
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



# Exemplo de uso para trocar 1 token Testnet (por exemplo, BNB na BSC Testnet) por outro token Testnet
token_in_address = '0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd'  # Endereço do token de entrada (por exemplo, BNB na BSC Testnet)
token_out_address = '0x8d008B313C1d6C7fE2982F62d32Da7507cF43551'  # Substitua pelo endereço do token de saída desejado na BSC Testnet
amount_in_tokens = 0.001  # Quantidade de tokens de entrada (por exemplo, 1 BNB)

transaction1_hash = approve_spending(token_in_address, pancakeswap_router_address, amount_in_tokens)
print("Transação enviada. Aprove:", transaction1_hash)
time.sleep(30) 
transaction2_hash = swap_tokens(token_in_address, token_out_address, amount_in_tokens)
print("Transação enviada. Hash da transação:", transaction2_hash)

