import json
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers.rpc import HTTPProvider


def connect_to_eth():
    url = "https://mainnet.infura.io/v3/cd2e3fb42f964a2bb6b835731b72bd84"
    w3 = Web3(HTTPProvider(url))
    assert w3.is_connected(), f"Failed to connect to provider at {url}"
    return w3


def connect_with_middleware(contract_json):
    with open(contract_json, "r") as f:
        d = json.load(f)
        d = d["bsc"]
        address = d["address"]
        abi = d["abi"]

    # Connect to BSC
    bnb_url = "https://bsc-dataseed.binance.org/"
    w3 = Web3(HTTPProvider(bnb_url))
    assert w3.is_connected(), f"Failed to connect to provider at {bnb_url}"

    # Inject middleware
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    # Create contract instance
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(address),
        abi=abi
    )

    return w3, contract


if __name__ == "__main__":
    connect_to_eth()
    w3, contract = connect_with_middleware("contract_info.json")
