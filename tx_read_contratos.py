from web3 import Web3
from dotenv import load_dotenv
import os

# Variáveis de ambiente
load_dotenv(".env")

# Configurar a conexão
provider_url = os.getenv('PROVIDER_URL')
web3 = Web3(Web3.HTTPProvider(provider_url))

abi_contrato = open("contrato_erc20.json", "r").read()

contract = web3.eth.contract(
    abi=abi_contrato, address=os.getenv('CONTRACT_ADDRESS'))

my_acc = os.getenv('MY_ACCOUNT')

balance = contract.functions.balanceOf(os.getenv('MY_ACCOUNT')).call()
balance_fmt = web3.from_wei(balance, "ether")

total_supply = web3.from_wei(contract.functions.totalSupply().call(), "ether")
print(f"O total de tokens emitidos é {total_supply}")
print('Contract Name: ', contract.functions.name().call())
print('Symbol: ', contract.functions.symbol().call())
print(f"Saldo da conta {my_acc}: {balance_fmt} {contract.functions.symbol().call()}")
