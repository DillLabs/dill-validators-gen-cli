from typing import Dict, NamedTuple
from .version import __version__
from eth_utils import decode_hex

DEPOSIT_CLI_VERSION = __version__


class BaseChainSetting(NamedTuple):
    NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes
    GENESIS_VALIDATORS_ROOT: bytes


MAINNET = 'mainnet'
GOERLI = 'goerli'
PRATER = 'prater'
SEPOLIA = 'sepolia'
ZHEJIANG = 'zhejiang'
HOLESKY = 'holesky'
DILL = 'dill'
ANDES = 'andes'
ALPS = 'alps'

# Mainnet setting
MainnetSetting = BaseChainSetting(
    NETWORK_NAME=MAINNET, GENESIS_FORK_VERSION=bytes.fromhex('00000000'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('4b363db94e286120d76eb905340fdd4e54bfe9f06bf33ff6cf5ad27f511bfe95'))
# Goerli setting
GoerliSetting = BaseChainSetting(
    NETWORK_NAME=GOERLI, GENESIS_FORK_VERSION=bytes.fromhex('00001020'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('043db0d9a83813551ee2f33450d23797757d430911a9320530ad8a0eabc43efb'))
# Sepolia setting
SepoliaSetting = BaseChainSetting(
    NETWORK_NAME=SEPOLIA, GENESIS_FORK_VERSION=bytes.fromhex('90000069'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('d8ea171f3c94aea21ebc42a1ed61052acf3f9209c00e4efbaaddac09ed9b8078'))
# Zhejiang setting
ZhejiangSetting = BaseChainSetting(
    NETWORK_NAME=ZHEJIANG, GENESIS_FORK_VERSION=bytes.fromhex('00000069'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('53a92d8f2bb1d85f62d16a156e6ebcd1bcaba652d0900b2c2f387826f3481f6f'))
# Holesky setting
HoleskySetting = BaseChainSetting(
    NETWORK_NAME=HOLESKY, GENESIS_FORK_VERSION=bytes.fromhex('01017000'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('9143aa7c615a7f7115e2b6aac319c03529df8242ae705fba9df39b79c59fa8b1'))
#Dill Mainnet setting
DillSetting = BaseChainSetting(
    NETWORK_NAME=DILL, GENESIS_FORK_VERSION=bytes.fromhex('01017550'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex('1234567890000000000000000000000000000000000000000000000000000000')) # ToDo: add genesisValitorsRoot when ready
# Andes setting
ANDES_GENESIS_VALIDATORS_ROOT_HEX='468ff3ea6b061b737d5f1bc35ab7b552a89c062efbb99fbad4420c614eecbab3'
AndesSetting = BaseChainSetting(
    NETWORK_NAME=ANDES, GENESIS_FORK_VERSION=bytes.fromhex('01017551'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex(ANDES_GENESIS_VALIDATORS_ROOT_HEX)
)

ALPS_GENESIS_VALIDATORS_ROOT_HEX='8f8a6d5d5926fac9a103bc6d7837d8cd224264c04c3164202664f8fb1f248f93'
AlpsSetting = BaseChainSetting(
    NETWORK_NAME=ALPS, GENESIS_FORK_VERSION=bytes.fromhex('01017552'),
    GENESIS_VALIDATORS_ROOT=bytes.fromhex(ALPS_GENESIS_VALIDATORS_ROOT_HEX)
)

ALL_CHAINS: Dict[str, BaseChainSetting] = {
    #MAINNET: MainnetSetting,
    #GOERLI: GoerliSetting,
    #PRATER: GoerliSetting,  # Prater is the old name of the Prater/Goerli testnet
    #SEPOLIA: SepoliaSetting,
    #ZHEJIANG: ZhejiangSetting,
    #HOLESKY: HoleskySetting,
    #DILL: DillSetting,
    ANDES: AndesSetting,
    ALPS: AlpsSetting,
}


def get_chain_setting(chain_name: str = DILL) -> BaseChainSetting:
    return ALL_CHAINS[chain_name]


def get_devnet_chain_setting(network_name: str,
                             genesis_fork_version: str,
                             genesis_validator_root: str) -> BaseChainSetting:
    return BaseChainSetting(
        NETWORK_NAME=network_name,
        GENESIS_FORK_VERSION=decode_hex(genesis_fork_version),
        GENESIS_VALIDATORS_ROOT=decode_hex(genesis_validator_root),
    )
