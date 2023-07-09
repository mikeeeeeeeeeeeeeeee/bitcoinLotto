import requests
from hdwallet import BIP44HDWallet
from hdwallet.derivations import BIP44Derivation
from hdwallet.cryptocurrencies import BitcoinMainnet

def check_transactions(address):
    try:
        response = requests.get(f'https://blockchain.info/rawaddr/{address}')
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return 0
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return 0

    data = response.json()
    return data['n_tx']

def check_transactions_for_addresses(mnemonic, num_addresses=1):
    # Create BIP44HDWallet
    bip44_hdwallet = BIP44HDWallet(cryptocurrency=BitcoinMainnet)
    # Get from mnemonic
    bip44_hdwallet.from_mnemonic(mnemonic=mnemonic)

    for i in range(num_addresses):
        # Derive the wallet
        bip44_derivation = BIP44Derivation.from_path(f"m/44'/0'/0'/0/{i}")
        bip44_hdwallet.from_path(bip44_derivation)
        address = bip44_hdwallet.address()
        num_transactions = check_transactions(address)
        if num_transactions > 0:
            with open('addresses_with_transactions.txt', 'a') as f:
                f.write(f'Mnemonic: {mnemonic}, Address: {address}\n')
        print(f'Address: {address}, Number of Transactions: {num_transactions}')
        

from mnemonic import Mnemonic

# Instantiate a Mnemonic object
mnemo = Mnemonic("english")

while True:
    # Generate a 12-word mnemonic
    mnemonic = mnemo.generate(strength=128)  # 128 bits for 12 words
    print("Mnemonic:", mnemonic)

    # Check number of transactions for addresses
    check_transactions_for_addresses(mnemonic, 1)
