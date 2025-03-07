from eth_utils import to_checksum_address

import click
from staking_deposit.utils.intl import (
    closest_match,
    load_text,
)

FUNC_NAME = 'convert_checksum_address'
@click.command()
@click.pass_context
def convert_checksum_address(address: str):
    return to_checksum_address(address)
