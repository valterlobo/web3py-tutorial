# import dependencies
import pickle
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import os
import csv 
# Var load
load_dotenv(".env")


# instantiate a web3 remote provider
provider_url = os.getenv('PROVIDER_URL')
web3 = Web3(Web3.HTTPProvider(provider_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# latest block number
ending_blocknumber = web3.eth.block_number  # 55911766  


# starting  block number 
starting_blocknumber = ending_blocknumber -100   #55910728



# filter through blocks and look for transactions involving this address
blockchain_address = "<ACCOUNT ADDRESS>"


balance_wei = web3.eth.get_balance(blockchain_address)
balance_eth = web3.from_wei(balance_wei, "ether")
print(f"BALANCE: { blockchain_address } : {balance_eth} MATIC")


# create an empty dictionary we will add transaction data to
tx_dictionary = {}

def getTransactions(start, end, address):
    '''This function takes three inputs, a starting block number, ending block number
    and an Ethereum address. The function loops over the transactions in each block and
    checks if the address in the to field matches the one we set in the blockchain_address.
    '''
    print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}...")
   
    for x in range(start, end):
        #web3.eth.get_block(x , full_transactions=True) 
        print(x, "->" ,start, end)
        block = web3.eth.get_block(x, True)
        for transaction in block.transactions:
            if transaction['to'] == address or transaction['from'] == address:
                print("-------------")                      
                print( transaction['hash'].hex(), transaction['from'] , transaction['to'] , transaction['value'])
                hashStr = transaction['hash'].hex()
                tx_dictionary[hashStr] = transaction

    print(f"Finished searching blocks {start} through {end} and found {len(tx_dictionary)} transactions")
    
    #write 
    with open('transaction.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["TX", "FROM", "TO" , "VALUE"]
        writer.writerow(field)
        for tx in tx_dictionary.values():
            writer.writerow([tx['hash'].hex(),  tx['from']  ,  tx['to'] , web3.from_wei( tx['value'], "ether")])
    file.close()           


getTransactions(starting_blocknumber, ending_blocknumber, blockchain_address)