from web3 import Web3
web3 = Web3(Web3.HTTPProvider('https://rpc.buildbear.io/multiple-jek-tono-porkins-7d39950a'))
print(web3.isConnected())
print(web3.eth.blockNumber)
account = "0xc144cD60Be02F5d5C6CFfcb56DcE32D99097Afb9"
balance = web3.eth.getBalance("0xc144cD60Be02F5d5C6CFfcb56DcE32D99097Afb9")
print(web3.fromWei(balance, "ether"))