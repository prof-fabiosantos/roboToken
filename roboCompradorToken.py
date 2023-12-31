from web3 import Web3
import time
import json

# Configurar a conexão com a rede Ethereum
web3 = Web3(Web3.HTTPProvider('https://rpc.buildbear.io/multiple-jek-tono-porkins-7d39950a'))
print("O Bot está conectado:"+str(web3.isConnected()))
#print("Número do Bloco:"+str(web3.eth.blockNumber))

chain_id = 9234

# Chaves privadas e endereços Ethereum
account = "0x2c24d0B31583912a9461FC95DFc200B53bca4e6A"
private_key = 'c58517d6dfc740985bb51e0293c6d5dce4ddbfa730edd097ca70d3e877e8b21e'

# Endereço e ABI do contrato TokenMarketplace
contract_Address = '0xB47bea8b9De7699F38f09864356117737980eDB2'  # Substitua pelo endereço do contrato TokenMarketplace
contract_abi = json.loads('[ 	{ 		"inputs": [ 			{ 				"internalType": "uint256", 				"name": "amount", 				"type": "uint256" 			} 		], 		"name": "buyTokens", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "uint256", 				"name": "amount", 				"type": "uint256" 			} 		], 		"name": "sellTokens", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "address", 				"name": "_token1Address", 				"type": "address" 			}, 			{ 				"internalType": "address", 				"name": "_token2Address", 				"type": "address" 			} 		], 		"stateMutability": "nonpayable", 		"type": "constructor" 	}, 	{ 		"inputs": [ 			{ 				"internalType": "uint256", 				"name": "amount", 				"type": "uint256" 			} 		], 		"name": "withdrawTokens", 		"outputs": [], 		"stateMutability": "nonpayable", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "getPrice", 		"outputs": [ 			{ 				"internalType": "uint256", 				"name": "", 				"type": "uint256" 			} 		], 		"stateMutability": "pure", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "ownerToken1", 		"outputs": [ 			{ 				"internalType": "address", 				"name": "", 				"type": "address" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "token1Address", 		"outputs": [ 			{ 				"internalType": "address", 				"name": "", 				"type": "address" 			} 		], 		"stateMutability": "view", 		"type": "function" 	}, 	{ 		"inputs": [], 		"name": "token2Address", 		"outputs": [ 			{ 				"internalType": "address", 				"name": "", 				"type": "address" 			} 		], 		"stateMutability": "view", 		"type": "function" 	} ]')

# Limiar de preço para comprar ou vender tokens
buy_threshold = 1.0  # Substitua pelo limiar de preço desejado para compra

# Criar uma instância do contrato TokenMarketplace
contract = web3.eth.contract(address=contract_Address, abi=contract_abi)

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


def get_token_price():
    # Implementar a lógica para obter o preço atual do token
    # Retorne o preço atual do token como um número em formato float
    # Por exemplo, você pode usar uma API externa para obter o preço ou calcular localmente com base em dados disponíveis
    # Aqui está um exemplo fictício que retorna um valor aleatório entre 1.0 e 3.0:
    import random
    return round(random.uniform(0, 2.0), 2)


# Exemplo de uso
if __name__ == '__main__':
    stop_order = False  # Variável para controlar a ordem de parada do robô

    print("Olá sou o Bot Comprador de Token, para interromper o robô pressione ao mesmo tempo CTRL + C")
    time.sleep(5)
    while not stop_order:
        token_price = get_token_price()
        print("Preço do Token:"+str(token_price))
        time.sleep(5)
        if token_price <= buy_threshold:
            print("O Preço é menor que o limiar de compra de "+str(buy_threshold))
            print("Portanto, vou comprar token")
            # Comprar tokens se o preço estiver abaixo ou igual ao limiar de compra
            buy_tokens(100)  # Substitua pelo valor desejado para compra
        else:
            print("Não irei comprar porque o preço está acima do limiar de compra:")


        # Aguardar um tempo antes de verificar novamente o preço
        time.sleep(20)  # Substitua pelo intervalo desejado em segundos
        
        
