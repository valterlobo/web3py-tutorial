from web3 import Web3
from dotenv import load_dotenv
import os

# Variáveis de ambiente
load_dotenv(".env")

# Configurar a conexão
provider_url = os.getenv('PROVIDER_URL')
web3 = Web3(Web3.HTTPProvider(provider_url))


# Consultando informações da blockchain
latest_block = web3.eth.block_number 
print(f"Número do bloco mais recente: {latest_block}")

# Obter saldo de uma conta Ethereum
account_address = os.getenv('MY_ACCOUNT') # Substitua pelo endereço desejado
balance_wei = web3.eth.get_balance(account_address)
balance_eth = web3.from_wei(balance_wei, "ether")
print(f"Saldo da conta {account_address}: {balance_eth} ETH")