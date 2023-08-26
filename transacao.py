from web3 import Web3
from dotenv import load_dotenv
import os

# Variáveis de ambiente
load_dotenv(".env")

# Configurar a conexão
provider_url = os.getenv('PROVIDER_URL')
web3 = Web3(Web3.HTTPProvider(provider_url))

from_address = os.getenv('MY_ACCOUNT')
to_address = os.getenv('TO_ADDRESS')
amount = "0.1"
# MUITO CUIDADO SEMPRE UTILIZAR CONTA DE TESTE
private_key = os.getenv('PRIVATE_KEY')

tx = {
    'type': '0x2',
    'nonce': web3.eth.get_transaction_count(from_address),
    'from': from_address,
    'to': to_address,
    'value': web3.to_wei(amount, 'ether'),
    'maxFeePerGas': web3.to_wei('250', 'gwei'),
    'maxPriorityFeePerGas': web3.to_wei('3', 'gwei'),
    'chainId': 80001
}

gas = web3.eth.estimate_gas(tx)
tx['gas'] = gas

# Assinatura
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
# ENVIO DA TRANSACAO
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
# ESPERAR PARA FINALIZAR
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# VERIFICAR
if tx_receipt['status'] == 1:
    print('ETH transferido com sucesso! Hash: {}'.format(
        str(web3.to_hex(tx_hash))))
else:
    print('Ocorreu um erro na transferência')
