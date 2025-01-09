from web3.contract import Contract

from app.config import AggregatorV3Interface_abi, AccessControlledOCR2Aggregator_abi
from app.services.web3_service import Web3Service
from app.services.etherscan_service import EtherscanService


class ChainlinkService:
    """
    Service for receiving and processing data from Chainlink Oracle Price Feed.
    """

    def __init__(
            self,
            web3_service: Web3Service,
            etherscan_service: EtherscanService,
            aggregator_proxy_address: str
    ):
        self.web3_service = web3_service
        self.etherscan_service = etherscan_service

        self.aggregator_proxy_abi = AggregatorV3Interface_abi
        self.aggregator_abi = AccessControlledOCR2Aggregator_abi

        # Initializing a proxy contract
        self.proxy_contract: Contract = self.web3_service.get_contract(
            address=aggregator_proxy_address,
            abi=self.aggregator_proxy_abi
        )

        # Getting the address of a real aggregator
        self.real_aggregator_address = self.proxy_contract.functions.aggregator().call()

        # Initializing a real aggregator contract
        self.aggregator_contract: Contract = self.web3_service.get_contract(
            address=self.real_aggregator_address,
            abi=self.aggregator_abi
        )

    def get_chainlink_price_at_timestamp(self, timestamp: int, block_range: int = 2000) -> float:
        """
        Gets the nearest price from the Chainlink Oracle Price Feed for a given timestamp.

        :param timestamp: Unix timestamp (integer representing seconds since epoch).
        :param block_range: Number of blocks to look before and after the target block. Defaults to 2000.

        :return: Price in float.
        """
        try:
            # Get the block closest to the timestamp
            block_for_ts = self.etherscan_service.get_block_by_timestamp(timestamp, closest='before')

            # Define the range of blocks
            start_block = max(block_for_ts - block_range, 0)
            end_block = min(block_for_ts + block_range, self.web3_service.w3.eth.block_number)

            # Getting event logs AnswerUpdated
            logs = self.aggregator_contract.events.AnswerUpdated().get_logs(
                from_block=start_block,
                to_block=end_block
            )

            if not logs:
                raise ValueError(
                    "There are no AnswerUpdated events in the given block range."
                )

            # Sort logs by updatedAt
            logs_sorted = sorted(logs, key=lambda event: event['args']['updatedAt'])

            # Looking for the last event where updatedAt <= timestamp
            candidate_event = None
            for event in logs_sorted:
                event_time = event['args']['updatedAt']
                if event_time <= timestamp:
                    candidate_event = event
                else:
                    break

            if not candidate_event:
                raise ValueError(
                    "No AnswerUpdated event found with updatedAt <= given timestamp."
                )

            # Get the price and convert it to float
            raw_price = candidate_event['args']['current']
            decimals = self.aggregator_contract.functions.decimals().call()
            price_float = raw_price / 10 ** decimals

            return price_float

        except ValueError as ve:
            raise ve

        except Exception as e:
            raise Exception(f"Unable to get price: {e}") from e
