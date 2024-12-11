pip install web3
!pip install protobuf==4.21.9
!pip install google-cloud-vision
!pip freeze | grep protobuf
pip install --upgrade jsonschema
pip install --upgrade pip
pip install solc
pip install py-solc-x
from solcx import compile_standard, install
pip install python-dotenv


#Importing required libraries
import json
import solcx
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from solcx import compile_standard
load_dotenv()
with open(
    r"C:\Users\S Nithin Reddy\OneDrive\Desktop\intern\SimpleStorageContract.sol",
    "r",
) as file:
    simple_storage_file = file.read()

install_solc("0.6.0")
simple_storage_file = """
pragma solidity ^0.6.0;
contract SimpleStorage {
    // State variable to store a single integer value
    uint256 public storedData;

    // Function to set the storedData value
    function set(uint256 x) public {
        storedData = x;
    }

    // Function to get the storedData value
    function get() public view returns (uint256) {
        return storedData;
    }

    // Function to store a value
    function store(uint256 _value) public {
        storedData = _value;
    }

    // Function to retrieve the stored value
    function retrieve() public view returns (uint256) {
        return storedData;
    }
}
"""
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
contract_abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']
contract_bytecode = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']
confirmations=0
from web3 import Web3
# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# Connect to Ganache (replace 'http://127.0.0.1:7545' with your Ganache server URL)
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# Get the chain ID
chain_id = w3.eth.chain_id

print(f"Chain ID: {chain_id}")
#USER ADDRESS
my_address = "" #This sender address and private key were taken from Ganache platform
#USER PRIVATE KEY
private_key = "" #This private key was taken from Ganache platform
SimpleStorage = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
nonce = w3.eth.get_transaction_count(my_address)
tx = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
import time
def times():
    a = time.time()
    print("Timestamp created at :",a )

    print("Time is (in GMT) : ",time.ctime(a))
    
times()



#Contract creation
signed_tx = w3.eth.account.sign_transaction(transaction_hash, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contract deployed to {tx_receipt.contractAddress}")
ts1,t1=times()
print("Timestamp created at :",ts1 )
print("Time is (in GMT) : ",t1)

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=contract_abi)

new_transaction = simple_storage.functions.store(25).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_new_txn = w3.eth.account.sign_transaction(
    new_transaction, private_key=private_key
)
tx_new_hash = 0x31990658c1d86843d6023301bf7b076ae3b48ac683bc5f7befc85ae5bff0ea41
#w3.eth.send_raw_transaction(signed_new_txn.rawTransaction)
print("Sending new transaction...")
# times()
tx_new_receipt = w3.eth.wait_for_transaction_receipt(tx_new_hash)

print(f"New stored value at Retrieve {simple_storage.functions.retrieve().call()}")
transaction_hash = "0x31990658c1d86843d6023301bf7b076ae3b48ac683bc5f7befc85ae5bff0ea41"

# Check transaction receipt
transaction_receipt = w3.eth.get_transaction_receipt(transaction_hash)

if transaction_receipt is not None:
    if transaction_receipt["status"] == 1:
        print("Transaction successful!")
    else:
        print("Transaction failed.")
else:
    print("Transaction not yet mined.")

# Wait for 3 confirmations
confirmations = 3
w3.eth.wait_for_transaction_receipt(transaction_hash, confirmations)
times()

transaction = w3.eth.get_transaction(transaction_hash)

print(f"From: {transaction['from']}")
print(f"To: {transaction['to']}")
print(f"Gas Used: {transaction['gas']}")

from web3 import Web3

# Connect to Ganache or Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Update the URL to your Ethereum node or Ganache instance

# Replace with your transaction hash
transaction_hash = "0x31990658c1d86843d6023301bf7b076ae3b48ac683bc5f7befc85ae5bff0ea41"

# Get transaction details
transaction = w3.eth.get_transaction(transaction_hash)

# Convert Wei to Ether
value_in_ether = w3.from_wei(transaction['value'], 'ether')

print(f"Value transferred in the transaction: {value_in_ether} Ether")

from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# Connect to Ganache or Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Replace with your node's URL

# Inject POA middleware for Ganache (If you're using a POA network)
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

# Check connection
if not w3.is_connected():  # Ensure that you're using the correct property
    raise Exception("Failed to connect to Ethereum node")

# Replace with your private keys and account addresses
sender_private_key = "0xee31856ec8ed75653e5796ea929bb48f669b04e059d8a469666782a2558a5269"
receiver_address = "0x0BCa9391Bf7ace211Bb28d5f127A82a477223A90"  # Replace with the actual receiver address

# Set the default account to use for transactions
sender_address = w3.eth.account.from_key(sender_private_key).address
w3.eth.default_account = sender_address

# Specify the amount of Ether to transfer (in Ether)
amount_to_transfer = 50.0

# Convert Ether to Wei
amount_in_wei = w3.to_wei(amount_to_transfer, 'ether')

# Check sender's balance
sender_balance = w3.eth.get_balance(sender_address)
print(f"Sender's balance: {w3.from_wei(sender_balance, 'ether')} Ether")

# Ensure the sender has enough balance
if sender_balance < amount_in_wei:
    raise Exception("Insufficient balance to send the transaction")

# Build the transaction
transaction = {
    'to': receiver_address,
    'value': amount_in_wei,
    'gas': 21000,
    'gasPrice': w3.to_wei('50', 'gwei'),
    'nonce': w3.eth.get_transaction_count(sender_address),
}

# Estimate gas if needed (optional step to verify)
try:
    estimated_gas = w3.eth.estimate_gas(transaction)
    print(f"Estimated Gas: {estimated_gas}")
    # Adjust gas if necessary
    transaction['gas'] = estimated_gas
except Exception as e:
    print(f"Error estimating gas: {e}")
    transaction['gas'] = 21000  # Default gas if estimation fails

# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, sender_private_key)

# Send the transaction using the correct attribute
try:
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    print(f"Transaction sent. Transaction hash: {transaction_hash.hex()}")
except Exception as e:
    print(f"Error sending transaction: {e}")

from web3 import Web3

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Update the URL to your Ethereum node or Ganache instance

# Replace with your transaction hash
transaction_hash="0x6555970c2a5ea61afa68fa5dc8b20ea632842b38584ed3e74ce2997d876c5952"

# Get transaction details
transaction = w3.eth.get_transaction(transaction_hash)

# Convert Wei to Ether
value_in_ether = w3.from_wei(transaction['value'], 'ether')

print(f"Value transferred in the transaction: {value_in_ether} Ether")
times()
