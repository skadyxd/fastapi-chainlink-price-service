from web3 import Web3
from web3.contract import Contract

from typing import Any


class Web3Service:
    """
    Service for interaction with blockchain via web3
    """

    def __init__(self, rpc_url: str):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to Ethereum RPC at address {rpc_url}")

    def get_contract(self, address: str, abi: Any) -> Contract:
        checksum_address = self.w3.to_checksum_address(address)
        return self.w3.eth.contract(address=checksum_address, abi=abi)
