from web3 import Web3
import time
import json
import aiohttp
import asyncio
from datetime import datetime, timedelta

# Configurar a conexão com a rede Ethereum
web3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
print("O Bot está conectado:"+str(web3.isConnected()))
chain_id = 97

# Chaves privadas e endereços BSC Testnet
account = "0x2c24d0B31583912a9461FC95DFc200B53bca4e6A"
private_key = 'c58517d6dfc740985bb51e0293c6d5dce4ddbfa730edd097ca70d3e877e8b21e'

# Endereço e ABI do contrato de roteamento da PancakeSwap. 
contract_Address = '0xD99D1c33F9fC3444f8101754aBC46c52416550D1'  # Substitua pelo endereço do contrato TokenMarketplace
contract_abi = json.loads('[{   "inputs": [     {       "internalType": "uint256",       "name": "amountIn",       "type": "uint256"     },     {       "internalType": "uint256",       "name": "amountOutMin",       "type": "uint256"     },     {       "internalType": "address[]",       "name": "path",       "type": "address[]"     },     {       "internalType": "address",       "name": "to",       "type": "address"     },     {       "internalType": "uint256",       "name": "deadline",       "type": "uint256"     }   ],   "name": "swapExactTokensForTokens",   "outputs": [     {       "internalType": "uint256[]",       "name": "amounts",       "type": "uint256[]"     }   ],   "stateMutability": "nonpayable",   "type": "function" }]')


# Limiar de preço para vender tokens
sell_threshold = 1.5  # Substitua pelo limiar de preço desejado para venda

# Criar uma instância do contrato de roteamento da PancakeSwap.
router_contract = web3.eth.contract(address=contract_Address, abi=contract_abi)


# Realizar a troca de tokens usando a função swapExactTokensForTokens
def sell_tokens(amount_to_sell, token_in_address, token_out_address):
    path = [token_in_address, token_out_address]

    # Converter a quantidade para Wei (a menor unidade do Ether)
    value = Web3.toWei(amount_to_sell, 'ether')

    # Converter 10 gwei para Wei (a menor unidade do Ether)
    gas_price_gwei = 10
    gas_price_wei = web3.toWei(gas_price_gwei, 'gwei')

    # Obter o timestamp atual em milissegundos
    timestamp_atual = int(datetime.now().timestamp() * 1000)
    # Adicionar 10000 milissegundos ao timestamp atual
    timestamp_futuro = timestamp_atual + 10000

    transaction = router_contract.functions.swapExactTokensForTokens(
        value,
        0,  # amountOutMin: Quantidade mínima desejada do token de saída (definido como 0 para troca exata)
        path,
        account,
        timestamp_futuro
    ).buildTransaction({        
        'gasPrice': gas_price_wei,  # Preço do gás adequado para a transação
        'gasLimit': 300000,
        "chainId": chain_id,
        'from': account,
        'nonce': web3.eth.getTransactionCount(account),  # Número de transação adequado para a carteira
    })
    # Assinar a transação com a chave privada
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    # Enviar a transação assinada para a rede BSC Testnet
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Aguardar a confirmação da transação
    web3.eth.wait_for_transaction_receipt(tx_hash)


TOKEN_OUT = "0x55d398326f99059fF775485246999027B3197955"

async def get_price(token_symbol):
    async with aiohttp.ClientSession() as session:
        url = f"https://bsc.api.0x.org/swap/v1/price?sellToken={token_symbol}&buyToken={TOKEN_OUT}&sellAmount=1000000000000000000"
        async with session.get(url) as response:
            data = await response.json()
            if "price" in data:
                return float(data["price"])
            else:
                raise ValueError("Price not found in API response")

PROFITABILITY = 1.1;#10% - define o percentual de lucro que você quer ter em cima da compra

# Exemplo de uso
# A cada laço o seu bot monitora o preço chamando a API e se o preço estiver acima
# do preço de venda mais uma lucratividade (10% no exemplo),
# o bot efetua a venda e imprime uma mensagem.
BNB = "0x2c24d0B31583912a9461FC95DFc200B53bca4e6A"
WBNB = "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd"
CAKE = "0x8d008B313C1d6C7fE2982F62d32Da7507cF43551"
USDT = "0x55d398326f99059fF775485246999027B3197955"

async def main():
    stop_order = False  # Variável para controlar a ordem de parada do robô

    print("Olá sou o Robô Vendedor de Token, para interromper o bot pressione ao mesmo tempo CTRL + C")
    time.sleep(5)
    while not stop_order:
        token_symbol = "BNB"
        try:
            token_price = await get_price(token_symbol)        
            print("Preço do Token:"+str(token_price))
        except Exception as e:
            print("Error:", str(e))
        time.sleep(5) 

        if token_price >= (sell_threshold * PROFITABILITY):
            # Vender tokens se o preço estiver acima ou igual ao limiar de venda
            print("O Preço é maior que o limiar de venda de "+str(sell_threshold))
            print("Portanto, vou vender token")

            sell_tokens(50,BNB,CAKE)  # Substitua pelo valor desejado para venda
        
        else:
            print("Não irei vender porque o preço está abaixo do limiar de venda:")

        # Aguardar um tempo antes de verificar novamente o preço
        time.sleep(20)  # Substitua pelo intervalo desejado em segundos


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
        
        
