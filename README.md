## Web3.py: Desenvolvendo app clientes para Ethereum com Python

Web3.py é uma biblioteca Python para interagir com a blockchain Ethereum. Ela fornece uma API simples e poderosa para realizar tarefas como consultar o estado da blockchain, enviar transações e interagir com contratos inteligentes.Neste tutorial, você aprenderá os conceitos básicos do Web3.py e como usá-lo para interagir com contratos inteligentes Ethereum e realizar operações na blockchain.

**Requisitos**

Para usar o Web3.py, você precisará do seguinte:

* Uma conta Ethereum com um saldo de ETH
* Um software cliente Ethereum, como o Mist ou o Geth
* Python 3.6 ou superior
* O pip package manager

**Instalação**

Para instalar o Web3.py, abra um terminal e execute o seguinte comando:

```
pip install web3
```
 obs instalar a lib auxiliar:
```
 pip install python-dotenv
```

**Configuração**

Para configurar o Web3.py, você precisará criar uma instância do Web3. Para fazer isso, você precisará do endereço do nó Ethereum que deseja conectar. Você pode encontrar uma lista de nós públicos aqui: https://infura.io/

```Python
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
```

**Consultando informações da blockchain**

Uma vez que você tenha configurado o Web3.py, você pode começar a consultar informações da blockchain. Para fazer isso, você pode usar os métodos da API do Web3.py, como `eth.get_balance()` e `eth.get_transaction_receipt()`.

```python

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

```

**Enviando transações**

Você também pode usar o Web3.py para enviar transações. Para fazer isso, você precisará criar uma transação e assiná-la com sua chave privada.

```python
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

# ASSINATURA
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

```

**Interagindo com contratos inteligentes**

Você pode usar o Web3.py para interagir com contratos inteligentes. Para fazer isso, você precisará primeiro compilar o contrato inteligente e obter seu ABI. Em seguida, você pode criar uma instância do contrato inteligente e chamar seus métodos.

```python
  # Importar o contrato e ABI
contract_address = "0xContractAddress"  # Substitua pelo endereço do seu contrato
contract_abi = [...]  # Substitua pelo ABI do seu contrato

# Criar um objeto de contrato
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Chamar uma função do contrato
result = contract.functions.someFunction().call()
print(f"Resultado da função do contrato: {result}")

# Enviar uma transação para o contrato (se a função modificar o estado)
transaction = {
    "from": "0xYourAddress",
    "gas": 2000000,  # A quantidade de gás pode variar
    "gasPrice": web3.toWei("50", "gwei"),  # Preço do gás em Gwei
}

transaction_hash = contract.functions.someFunction().transact(transaction)
print(f"Hash da transação: {transaction_hash.hex()}")

```

**Como ler a informação de um contrato ERC20**

Este código irá imprimir o saldo da conta Ethereum especificada na variável MY_ACCOUNT e o total de tokens emitidos pelo contrato.

```Python
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
```

**Como enviar uma transação para um contrato ERC20**

Este código irá enviar 10 tokens ERC-20 da conta Ethereum especificada na variável MY_ACCOUNT para a conta especificada na variável TO_ADDRESS.

```Python
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
```

**_Observações_**

Para enviar uma transação, você precisará de sua chave privada. Você pode encontrar sua chave privada em sua carteira Ethereum.
Se você estiver usando uma rede de teste você precisará de uma conta de teste.
