import json
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers.rpc import HTTPProvider

def connect_to_eth():
    url = "https://mainnet.infura.io/v3/cd2e3fb42f964a2bb6b835731b72bd84"
    w3 = Web3(HTTPProvider(url))
    assert w3.is_connected(), f"Failed to connect to provider at {url}"
    print("Connected to Ethereum mainnet")
    print("Latest block:", w3.eth.block_number)
    return w3

def connect_with_middleware(contract_json):
    with open(contract_json, "r") as f:
        data = json.load(f)
        bsc_data = data['bsc']
        address = bsc_data['address']
        abi = bsc_data['abi']

    bnb_testnet_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
    w3 = Web3(HTTPProvider(bnb_testnet_url))
    assert w3.is_connected(), f"Failed to connect to BNB testnet at {bnb_testnet_url}"

    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(address),
        abi=abi
    )

    print("Connected to BNB testnet")
    print("Chain ID:", w3.eth.chain_id)
    print("Latest block:", w3.eth.block_number)
    print("Contract object created successfully")

    return w3, contract

if __name__ == "__main__":
    eth_w3 = connect_to_eth()
    bsc_w3, contract = connect_with_middleware("contract_info.json")
