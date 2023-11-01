from spectral_sdk.config_manager import ConfigManager
from functools import wraps
from tqdm import tqdm
from web3 import Web3
import click
import os
import requests
# from . import CONFIG_PATH, ALCHEMY_URL, ABIS # works for pip package
from spectral_sdk import CONFIG_PATH, ALCHEMY_URL, ABIS # works for direct calling
import pandas as pd
import numpy as np
from spectral_sdk.ezkl_wrapper.ezkl_wrapper import dump_model

from retrying import retry
config_manager = None
@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_from_ipfs(cid, filename, file_type = "File"):
    primary_source = "http://ipfs.io/ipfs/"
    url = primary_source + cid

    try:
        # Make the GET request to fetch the file content
        response = requests.get(url, timeout=(3,8), stream=True)
        
        # Check if the request was successful
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8K
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        # Save the content to the specified file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                progress_bar.update(len(chunk))
        
        progress_bar.close()
        print(f"{file_type} successfully downloaded!")
        

    except requests.ReadTimeout as e:
        print("Failed to fetch the file from the official gateway. Trying another gateway...")
        response = requests.post("http://ipfs.dev.spectral.finance:5001/api/v0/cat?arg=" + cid)
        
        # Check if the request was successful
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192  # 8K
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        
        # Save the content to the specified file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                progress_bar.update(len(chunk))
        
        progress_bar.close()
        print(f"{file_type} successfully fetched from the alternative gateway!")


@click.group()
def cli():
    """Modelers SDK provides tools to interact with Spectral platform and taking part in competitions."""
    pass

import requests

def get_multisig_address(address):
    """
    Fetches the MultiSig address for a given address from the API.

    :param address: The address to query.
    :return: A string with the MultiSig address or None.
    """
    url = f"https://subscription-library.dev.spectral.finance/getMultiSigAddress/{address}"
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'message' in data and data['message'] == 'No data found':
            return None
        else:
            return data
    elif response.status_code == 404:
        return None


def ensure_global_config():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config_manager = ConfigManager(CONFIG_PATH)
            config_updated = False
            if config_manager.get('global', 'api_key') is None:
                click.echo("Input your Spectral API key.")
                click.echo("To get your Spectral API key, please visit https://app.spectral.dev/account")
                api_key = click.prompt("Spectral API key:")
                config_manager.set('global', 'api_key', api_key)
                config_updated = True
                click.echo("\n")
            if config_manager.get('global', 'alchemy_api_key') is None:
                click.echo("Input your Alchemy API key.")
                click.echo(
                    "To get your Alchemy API key, please visit https://www.alchemy.com/")
                alchemy_api_key = click.prompt("Alchemy API key:")
                config_manager.set('global', 'alchemy_api_key', alchemy_api_key)
                config_updated = True
                click.echo("\n")
            if config_manager.get('global', 'wallet_private_key') is None and config_manager.get('global', 'wallet_address') is None:
                from web3 import Web3
                from eth_account import Account
                # Initialize Web3
                w3 = Web3()
                # Generate a new account
                new_account = Account.create()

                # Extract the private key and address
                private_key = new_account._private_key.hex()
                address = new_account.address
                config_manager.set('global', 'wallet_private_key', private_key)
                config_manager.set('global', 'wallet_address', address)
                click.echo(f"A new wallet address has been generated for this machine. Navigate to https://app.spectral.finance/profile to connect local wallet with your main wallet.\n Paste the following address in the input field: {address}")
                config_updated = True
            if config_manager.get('global', 'wallet_private_key') and config_manager.get('global', 'multisig_wallet_address') is None:
                multisig_wallet_address = get_multisig_address(config_manager.get('global', 'wallet_address'))
                if multisig_wallet_address:
                    config_manager.set('global', 'wallet_address', address)
                    config_updated = True
                else:
                    click.echo("Your wallet address is not connected to any multisig wallet. Please connect your wallet to multisig wallet in your Spectral account profile page. https://app.spectral.finance/profile")
            if config_updated:
                click.echo("Config has been updated.")
            return func(config_manager, *args, **kwargs)
        return wrapper
    return decorator

@cli.command()
@ensure_global_config()
@click.argument('challenge_id')
def fetch_training_data(config_manager, challenge_id):
    """Fetches Training Dataset from IPFS."""
    competition_abi = ABIS['Competition']
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL + web3_provider_api_key))
    contract = w3.eth.contract(address=challenge_id, abi=competition_abi)
    ipfsTrainingDataset = contract.functions.ipfsTrainingDataset().call()
    filename = f"{challenge_id}_training_data.csv"
    fetch_from_ipfs(ipfsTrainingDataset, filename, "Training dataset")

@cli.command()
@ensure_global_config()
@click.argument('challenge_id')
@click.argument('wallet_address')
def fetch_testing_data(config_manager, challenge_id, wallet_address):
    """Configures datawrappers. To see available datawrappers run `spectral datawrappers`."""
    competition_abi = ABIS['Competition']
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL + web3_provider_api_key))
    contract = w3.eth.contract(address=challenge_id, abi=competition_abi)
    modeler_contract_address = contract.functions.modelerContract().call()
    modeler_abi = ABIS['Modeler']
    modeler_contract = w3.eth.contract(address=modeler_contract_address, abi=modeler_abi)
    modeller_challanges = modeler_contract.functions.modelerChallenges(wallet_address).call()
    ipfs_hash = modeller_challanges[0]
    fetch_from_ipfs(ipfs_hash, "testing_dataset.csv", "Training dataset")
    
@cli.command()
@ensure_global_config()
@click.argument('model_path')
@click.argument('input_json_path')
@click.argument('competition_address')
def commit(config_manager, model_path, input_json_path, competition_address):
    """Commit to a model using Multisig"""
    ipfs_api_key = config_manager.get('global', 'api_key')
    model_cid = dump_model(model_path, input_json_path, ipfs_api_key)
    
    destination_wallet_address_private_key = config_manager.get('global', 'wallet_private_key')
    destination_wallet_address = config_manager.get('global', 'wallet_address')
    multisig_wallet_address = config_manager.get('global', 'multisig_wallet_address')
    competition_abi = ABIS['Competition']
    modeler_abi = ABIS['Modeler']
    modeler_address = "0xAC689722AfB9887ce61B4c1677f5cb49293A1BbC"
    wallet_simple_abi = ABIS['WalletSimple']
    
    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider((ALCHEMY_URL + web3_provider_api_key)))
    current_block = w3.eth.block_number

    current_block_timestamp = w3.eth.get_block(current_block)['timestamp']
    competition_contract = w3.eth.contract(address=competition_address, abi=competition_abi)
    modeler_contract = w3.eth.contract(address=modeler_address, abi=modeler_abi)
    multisig_contract = w3.eth.contract(address=multisig_wallet_address, abi=w337allet_simple_abi)
    
    commit_function_data = {}
    contract_address = None
    if modeler_contract.functions.modelers(multisig_wallet_address).call()[0] == '':
        commit_function_data = competition_contract.functions.signUpToCompetition(model_cid).build_transaction({
            'chainId': 5,
            'gas': 300000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(destination_wallet_address)
        })['data']
        contract_address = competition_address
    else:
        commit_function_data = modeler_contract.functions.updateModel(model_cid).build_transaction({
            'chainId': 5,
            'gas': 300000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(destination_wallet_address)
        })['data']
        contract_address = modeler_address
    
    import time
    next_sequence_id = multisig_contract.functions.getNextSequenceId().call()
    expire_time = int(time.time()) + 3600  # Current time + 1 hour
    sequence_id = next_sequence_id
    signature = '0x'  # No signature needed for a 1-2 multisig
    
    txn_details = {
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    }
    multisig_txn = multisig_contract.functions.sendMultiSig(
        contract_address,
        0,
        commit_function_data,
        expire_time,
        sequence_id,
        signature
    ).build_transaction(txn_details)
    
    private_key = destination_wallet_address_private_key
    signed_multisig_txn = w3.eth.account.sign_transaction(multisig_txn, private_key)

    try:
        multisig_txn_hash = w3.eth.send_raw_transaction(signed_multisig_txn.rawTransaction)
        multisig_txn_receipt = w3.eth.wait_for_transaction_receipt(multisig_txn_hash)
        print('Commiting to a model completed with receipt:', multisig_txn_receipt.__dict__)
        multisig_txn_receipt
    except Exception as e:
        print("Transaction failed with error:", str(e))


@cli.command()
@ensure_global_config()
@click.argument('competition_address')
@click.argument('submission_file')
def submit_inferences(config_manager, competition_address, submission_file):
    destination_wallet_address_private_key = config_manager.get('global', 'wallet_private_key')
    destination_wallet_address = config_manager.get('global', 'wallet_address')
    multisig_wallet_address = config_manager.get('global', 'multisig_wallet_address')
    spectral_token_abi = ABIS['SpectralToken']
    wallet_simple_abi = ABIS['WalletSimple']

    web3_provider_api_key = config_manager.get('global', 'alchemy_api_key')
    w3 = Web3(Web3.HTTPProvider((ALCHEMY_URL + web3_provider_api_key)))
    
    token_contract = w3.eth.contract(address=token_contract_address, abi=spectral_token_abi)
    multisig_contract = w3.eth.contract(address=multisig_wallet_address, abi=wallet_simple_abi)

    approve_function_data = token_contract.functions.approve(competition_contract_address, int(amount)).build_transaction({'chainId': 5,  # or whatever chain you're using
        'gas': 30000000,
        'gasPrice': w3.to_wei('2000', 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)})['data']
    import time
    next_sequence_id = multisig_contract.functions.getNextSequenceId().call()
    expire_time = int(time.time()) + 3600  # Current time + 1 hour
    sequence_id = next_sequence_id
    signature = '0x'  # No signature needed for a 1-2 multisig

    multisig_txn = multisig_contract.functions.sendMultiSig(
        token_contract_address,
        0,
        approve_function_data,
        expire_time,
        sequence_id,
        signature
    ).build_transaction({
        'chainId': 5,
        'gas': 150000,
        'gasPrice': w3.to_wei('100', 'gwei'),
        'nonce': w3.eth.get_transaction_count(destination_wallet_address)
    })
    pass

@cli.command()
@ensure_global_config()
def configure(config_manager):
    """Configures datawrappers. To see available datawrappers run `spectral datawrappers`."""
    click.echo(f"Spectral SDK is configured!")

if __name__ == '__main__':
    cli()
    pass
