from web3 import Web3
from dotenv import load_dotenv
import os

# Variáveis de ambiente
load_dotenv(".env")

# Configurar a conexão com o Ganache (ou outro endpoint Ethereum)
provider_url = os.getenv('PROVIDER_URL')
web3 = Web3(Web3.HTTPProvider(provider_url))

# Verificar a conexão
if web3.is_connected():
    print("Conectado à rede Ethereum")
else:
    print("Não foi possível conectar à rede Ethereum. Verifique o URL.")
