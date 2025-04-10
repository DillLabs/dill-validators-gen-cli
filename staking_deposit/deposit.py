import click
import sys

from staking_deposit.cli.existing_mnemonic import existing_mnemonic
from staking_deposit.cli.generate_bls_to_execution_change import generate_bls_to_execution_change
from staking_deposit.cli.new_mnemonic import new_mnemonic
from staking_deposit.cli.generate_mnemonic import generate_mnemonic
from staking_deposit.cli.convert_checksum_address import convert_checksum_address
from staking_deposit.utils.click import (
    captive_prompt_callback,
    choice_prompt_func,
    jit_option,
)
from staking_deposit.utils import config
from staking_deposit.utils.constants import INTL_LANG_OPTIONS
from staking_deposit.utils.intl import (
    get_first_options,
    fuzzy_reverse_dict_lookup,
    load_text,
)


def check_python_version() -> None:
    '''
    Checks that the python version running is sufficient and exits if not.
    '''
    if sys.version_info < (3, 7):
        click.pause(load_text(['err_python_version']))
        sys.exit()


@click.group()
@click.pass_context
@click.option(
    '--non_interactive',
    default=False,
    is_flag=True,
    help='Disables interactive prompts. Warning: with this flag, there will be no confirmation step(s) to verify the input value(s). Please use it carefully.',  # noqa: E501
    hidden=False,
)
def cli(ctx: click.Context, non_interactive: bool) -> None:
    config.language = 'English'  # Set language to English
    config.non_interactive = non_interactive  # Remove interactive commands


cli.add_command(existing_mnemonic)
cli.add_command(new_mnemonic)
cli.add_command(generate_mnemonic)
cli.add_command(generate_bls_to_execution_change)
cli.add_command(convert_checksum_address)

if __name__ == '__main__':
    check_python_version()
    cli()
