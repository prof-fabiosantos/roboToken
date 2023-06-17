from web3 import Web3
import os
import time
import json

# Configurar a conexão com a rede Ethereum
web3 = Web3(Web3.HTTPProvider('https://rpc.buildbear.io/multiple-jek-tono-porkins-7d39950a'))
print("Está conectado:"+str(web3.isConnected()))
print("Número do Bloco:"+str(web3.eth.blockNumber))

chain_id = 9234

# Chaves privadas e endereços Ethereum
account = "0x2c24d0B31583912a9461FC95DFc200B53bca4e6A"
private_key = 'c58517d6dfc740985bb51e0293c6d5dce4ddbfa730edd097ca70d3e877e8b21e'

# Endereço e ABI do contrato TokenMarketplace
contract_Address = '0xa69811F48350A2C839eCED6b6b258200c427b7bB'  # Substitua pelo endereço do contrato TokenMarketplace
contract_abi = json.loads('[ 	{ 		"inputs": [ 			{ 				"internalType": "uint256", 				"name": "amount", 				"type": "uint256" 			} 		], 		"name": "buyTokens", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "uint256", 				"name": "amount", 				"type": "uint256" 			} 		], 		"name": "sellTokens", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "address", 				"name": "_token1Address", 				"type": "address" 			}, 			{ 				"internalType": "address", 				"name": "_token2Address", 				"type": "address" 			} 		], 		"stateMutability": "nonpayable", 		"type": "constructor" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "uint256", 				"name": "amount", 				"type": "uint256" 			} 		], 		"name": "withdrawTokens", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getPrice", 		"outputs": [ 			{ 				"internalType": "uint256", 				"name": "", 				"type": "uint256" 			} 		], 		"stateMutability": "pure", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "ownerToken1", 		"outputs": [ 			{ 				"internalType": "address", 				"name": "", 				"type": "address" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "token1Address", 		"outputs": [ 			{ 				"internalType": "address", 				"name": "", 				"type": "address" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "token2Address", 		"outputs": [ 			{ 				"internalType": "address", 				"name": "", 				"type": "address" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]')

# Limiar de preço para comprar ou vender tokens
buy_threshold = 1.0  # Substitua pelo limiar de preço desejado para compra
sell_threshold = 2.0  # Substitua pelo limiar de preço desejado para venda

# Criar uma instância do contrato TokenMarketplace
contract = web3.eth.contract(address=contract_Address, abi=contract_abi)

nonce = web3.eth.getTransactionCount(account)

def approve_token_spending(token_contract_address, amount):
    
    token_contract = web3.eth.contract(address=token_contract_address, abi=token_abi)
    approve_tx = token_contract.functions.approve(contract_Address, amount).buildTransaction({
        "gasPrice": web3.eth.gas_price,
        "chainId": chain_id,
        "from": account,
        "nonce": nonce
    })
    signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key=private_key)
    approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
    print("Aprovação de gastos enviada. Hash da transação:", web3.toHex(approve_tx_hash))


def buy_tokens(amount_to_buy):
    # Implementar a lógica para comprar tokens
    nonce = web3.eth.getTransactionCount(account)
    transaction = contract.functions.buyTokens(amount_to_buy).buildTransaction({
        "gasPrice": web3.eth.gas_price,
        "chainId": chain_id,
        "from": account,
        "nonce": nonce
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print('Compra de tokens enviada com sucesso. Hash da transação:', web3.toHex(tx_hash))


def sell_tokens(amount_to_sell):
    # Implementar a lógica para vender tokens
    transaction = contract.functions.sellTokens(amount_to_sell).buildTransaction({
        "gasPrice": web3.eth.gas_price,
        "chainId": chain_id,
        "from": account,
        "nonce": nonce
    })
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print('Venda de tokens enviada. Hash da transação:', web3.toHex(tx_hash))


def get_token_price():
    # Implementar a lógica para obter o preço atual do token
    # Retorne o preço atual do token como um número em formato float
    # Por exemplo, você pode usar uma API externa para obter o preço ou calcular localmente com base em dados disponíveis
    # Aqui está um exemplo fictício que retorna um valor aleatório entre 1.0 e 3.0:
    import random
    return round(random.uniform(1.0, 1.0), 2)


# Exemplo de uso
if __name__ == '__main__':
    stop_order = False  # Variável para controlar a ordem de parada do robô

    # 1. Aprovar o contrato TokenMarketplace para gastar tokens
    #token_contract_address = '0x8a1786e9D08c2E5C898343321DdE988e4bbdec0e'  # Substitua pelo endereço do contrato do token ERC-20
    #token_amount_to_approve = 700000  # Substitua pela quantidade de tokens que deseja aprovar
    #approve_token_spending(token_contract_address, token_amount_to_approve)
    print("Olá sou o Robô comprador de Token, para interromper o robô pressione ao mesmo tempo CTRL + C")

    while not stop_order:
        token_price = get_token_price()
        print("Preço do Token:"+str(token_price))

        if token_price <= buy_threshold:
            print("O Preço é menor que o limiar de compra de "+str(buy_threshold))
            print("Portanto, vou comprar token")
            # Comprar tokens se o preço estiver abaixo ou igual ao limiar de compra
            buy_tokens(100)  # Substitua pelo valor desejado para compra
            

        if token_price >= sell_threshold:
            # Vender tokens se o preço estiver acima ou igual ao limiar de venda
            sell_tokens(50)  # Substitua pelo valor desejado para venda

        # Aguardar um tempo antes de verificar novamente o preço
        time.sleep(60)  # Substitua pelo intervalo desejado em segundos
        
        
