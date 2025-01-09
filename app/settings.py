from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    WEB3_RPC_URL: str = ""
    ETHERSCAN_API_KEY: str = ""
    ETHERSCAN_BASE_URL: str = "https://api.etherscan.io/api"
    CHAINLINK_AGGREGATOR_PROXY_ADDRESS: str = ""

    class Config:
        env_file = ".env"
