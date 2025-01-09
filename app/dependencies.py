from fastapi import Depends

from app.services.chainlink_service import ChainlinkService
from app.services.etherscan_service import EtherscanService
from app.services.web3_service import Web3Service
from app.settings import Settings


def get_settings() -> Settings:
    return Settings()


def get_web3_service(settings: Settings = Depends(get_settings)) -> Web3Service:
    return Web3Service(rpc_url=settings.WEB3_RPC_URL)


def get_etherscan_service(settings: Settings = Depends(get_settings)) -> EtherscanService:
    return EtherscanService(
        api_key=settings.ETHERSCAN_API_KEY,
        base_url=settings.ETHERSCAN_BASE_URL
    )


def get_chainlink_service(
        web3_service: Web3Service = Depends(get_web3_service),
        etherscan_service: EtherscanService = Depends(get_etherscan_service),
        settings: Settings = Depends(get_settings)
) -> ChainlinkService:
    return ChainlinkService(
        web3_service=web3_service,
        etherscan_service=etherscan_service,
        aggregator_proxy_address=settings.CHAINLINK_AGGREGATOR_PROXY_ADDRESS,
    )
