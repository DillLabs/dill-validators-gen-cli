from eth_utils import to_checksum_address

import click
from staking_deposit.utils.intl import (
    closest_match,
    load_text,
)

FUNC_NAME = 'convert_checksum_address'

@click.command()
@click.option('--address', required=True, help='The Ethereum address to convert to checksum format')
@click.pass_context
def convert_checksum_address(ctx, address: str):
    checksum_address = to_checksum_address(address)
    click.echo(f'Checksum address: {checksum_address}')
    return checksum_address
