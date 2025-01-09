import requests


class EtherscanService:
    """
    Service for interacting with the Etherscan API.
    """

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_block_by_timestamp(self, timestamp: int, closest: str = 'before') -> int:
        """
        Queries Etherscan for the block number closest to the given Unix timestamp.
        """
        params = {
            "module": "block",
            "action": "getblocknobytime",
            "timestamp": str(timestamp),
            "closest": closest,
            "apikey": self.api_key
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        if data.get('status') == '1':
            return int(data.get('result'))
        else:
            raise Exception(f"Etherscan error: {data}")
