from web3 import Web3
from dotenv import load_dotenv
import os

# Variáveis de ambiente
load_dotenv(".env")

# Configurar a conexão
provider_url = os.getenv('PROVIDER_URL')
web3 = Web3(Web3.HTTPProvider(provider_url))

# Obtém o ABI do contrato
abi_contrato = open("contrato_erc20.json", "r").read()

# Cria uma instância do contrato
contract = web3.eth.contract(
    abi=abi_contrato, address=os.getenv('CONTRACT_ADDRESS'))

my_acc = os.getenv('MY_ACCOUNT')
balance = contract.functions.balanceOf(os.getenv('MY_ACCOUNT')).call()
balance_antes = web3.from_wei(balance, "ether")


# TRANSAÇÃO INICIO
from_address = my_acc
to_address = os.getenv('TO_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

amount_wei = web3.to_wei(10, 'ether')
print(f"Transferindo 10")

# Cria uma transação
tx = contract.functions.transfer(to_address, amount_wei).build_transaction({
    'from': from_address,
    'nonce': web3.eth.get_transaction_count(from_address),
    'maxFeePerGas': web3.to_wei('250', 'gwei'),
    'maxPriorityFeePerGas': web3.to_wei('3', 'gwei'),
    'value': 0,
    'chainId': 80001
})
gas = web3.eth.estimate_gas(tx)
tx['gas'] = gas

# Assina a transação
signed_tx = web3.eth.account.sign_transaction(tx, private_key)

# Envia a transação
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

if tx_receipt['status'] == 1:
    print('Tokens transferido com sucesso! Hash: {}'.format(
        str(web3.to_hex(tx_hash))))
else:
    print('Ocorreu um erro na transferência de tokens')


if tx_receipt['status'] == 1:
    balance = contract.functions.balanceOf(os.getenv('MY_ACCOUNT')).call()
    balance_depois = web3.from_wei(balance, "ether")
    total_supply = web3.from_wei(
        contract.functions.totalSupply().call(), "ether")
    print(f"O total de tokens emitidos é {total_supply}")
    print('Contract Name: ', contract.functions.name().call())
    print('Symbol: ', contract.functions.symbol().call())
    print(
        f"Saldo da conta antes   {my_acc}: {balance_antes} {contract.functions.symbol().call()}")
    print(
        f"Saldo da conta depois  {my_acc}: {balance_depois} {contract.functions.symbol().call()}")
