import os
import stat
import click
from typing import (
    Any,
    Callable,
)

from eth_typing import HexAddress
from staking_deposit.credentials import (
    CredentialList,
)
from staking_deposit.exceptions import ValidationError
from staking_deposit.utils.validation import (
    verify_deposit_data_json,
    validate_int_range,
    validate_password_strength,
    validate_eth1_withdrawal_address,
    validate_deposit_amount,
)
from staking_deposit.utils.constants import (
    MAX_DEPOSIT_AMOUNT,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from staking_deposit.utils.ascii_art import DILL_1
from staking_deposit.utils.click import (
    captive_prompt_callback,
    choice_prompt_func,
    jit_option,
)
from staking_deposit.utils.intl import (
    closest_match,
    load_text,
)
from staking_deposit.settings import (
    ALL_CHAINS,
    MAINNET,
    PRATER,
    get_chain_setting,
)


def get_password(text: str) -> str:
    return click.prompt(text, hide_input=True, show_default=False, type=str)


def generate_keys_arguments_decorator(function: Callable[..., Any]) -> Callable[..., Any]:
    '''
    This is a decorator that, when applied to a parent-command, implements the
    to obtain the necessary arguments for the generate_keys() subcommand.
    '''
    decorators = [
        jit_option(
            callback=captive_prompt_callback(
                lambda num: validate_int_range(num, 1, 2**32),
                lambda: load_text(['num_validators', 'prompt'], func='generate_keys_arguments_decorator')
            ),
            help=lambda: load_text(['num_validators', 'help'], func='generate_keys_arguments_decorator'),
            param_decls="--num_validators",
            prompt=lambda: load_text(['num_validators', 'prompt'], func='generate_keys_arguments_decorator'),
        ),
        jit_option(
            default=os.getcwd(),
            help=lambda: load_text(['folder', 'help'], func='generate_keys_arguments_decorator'),
            param_decls='--folder',
            type=click.Path(exists=True, file_okay=False, dir_okay=True),
        ),
        jit_option(
            callback=captive_prompt_callback(
                lambda x: closest_match(x, list(ALL_CHAINS.keys())),
                choice_prompt_func(
                    lambda: load_text(['chain', 'prompt'], func='generate_keys_arguments_decorator'),
                    list(ALL_CHAINS.keys())
                ),
            ),
            default=MAINNET,
            help=lambda: load_text(['chain', 'help'], func='generate_keys_arguments_decorator'),
            param_decls='--chain',
            prompt=choice_prompt_func(
                lambda: load_text(['chain', 'prompt'], func='generate_keys_arguments_decorator'),
                list(key for key in ALL_CHAINS.keys() if key != PRATER)
            ),
        ),
        jit_option(
            callback=captive_prompt_callback(
                validate_password_strength,
                lambda:load_text(['keystore_password', 'prompt'], func='generate_keys_arguments_decorator'),
                #lambda:load_text(['keystore_password', 'confirm'], func='generate_keys_arguments_decorator'),
                None,
                #lambda: load_text(['keystore_password', 'mismatch'], func='generate_keys_arguments_decorator'),
                None,
                True,
            ),
            help=lambda: load_text(['keystore_password', 'help'], func='generate_keys_arguments_decorator'),
            hide_input=True,
            param_decls='--keystore_password',
            prompt=lambda: load_text(['keystore_password', 'prompt'], func='generate_keys_arguments_decorator'),
        ),
        jit_option(
            callback=captive_prompt_callback(
                lambda address: validate_eth1_withdrawal_address(None, None, address),
                lambda: load_text(['arg_execution_address', 'prompt'], func='generate_keys_arguments_decorator'),
                #lambda: load_text(['arg_execution_address', 'confirm'], func='generate_keys_arguments_decorator'),
                #lambda: load_text(['arg_execution_address', 'mismatch'], func='generate_keys_arguments_decorator'),
            ),
            default=None,
            help=lambda: load_text(['arg_execution_address', 'help'], func='generate_keys_arguments_decorator'),
            param_decls=['--execution_address', '--eth1_withdrawal_address'],
        ),
        jit_option(
            callback=captive_prompt_callback(
                lambda deposit_amount: validate_deposit_amount(deposit_amount),
                lambda: load_text(['deposit_amount', 'prompt'], func='generate_keys_arguments_decorator'),
            ),
            default=3600,
            help=lambda: load_text(['deposit_amount', 'help'], func='generate_keys_arguments_decorator'),
            param_decls="--deposit_amount",
            prompt=lambda: load_text(['deposit_amount', 'prompt'], func='generate_keys_arguments_decorator'),
        ),
        click.option('--save_password', is_flag=True, default=False, help='Save the keystore password to a file.'),
        click.option('--save_mnemonic', is_flag=True, default=False, help='Save the mnemonic to a file.'),
    ]
    for decorator in reversed(decorators):
        function = decorator(function)
    return function


@click.command()
@click.pass_context
def generate_keys(ctx: click.Context, validator_start_index: int,
                    num_validators: int, folder: str, chain: str, keystore_password: str,
                    execution_address: HexAddress, deposit_amount: int, save_password: bool,
                    save_mnemonic: bool, **kwargs: Any) -> None:
    import time
    current_time = int(time.time())  # Generate a unified timestamp
    mnemonic = ctx.obj['mnemonic']
    mnemonic_password = ctx.obj['mnemonic_password']
    amounts = [deposit_amount] * num_validators
    folder = os.path.join(folder, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)
    chain_setting = get_chain_setting(chain)
    if not os.path.exists(folder):
        os.mkdir(folder)
    click.clear()
    click.echo(DILL_1)
    click.echo(load_text(['msg_key_creation']))
    credentials = CredentialList.from_mnemonic(
        mnemonic=mnemonic,
        mnemonic_password=mnemonic_password,
        num_keys=num_validators,
        amounts=amounts,
        chain_setting=chain_setting,
        start_index=validator_start_index,
        hex_eth1_withdrawal_address=execution_address,
    )
    keystore_filefolders = credentials.export_keystores(password=keystore_password, folder=folder, timestamp=current_time)
    deposits_file = credentials.export_deposit_data_json(folder=folder, timestamp=current_time)  # Use unified timestamp
    if save_password:
        credentials.save_password(password=keystore_password, folder=folder, timestamp=current_time)
    if save_mnemonic:
        mnemonic_file_path = os.path.join(folder, f'mnemonic-{current_time}.txt')  # Use unified timestamp
        with open(mnemonic_file_path, 'w') as f:
            f.write(mnemonic)
        if os.name == 'posix':
            os.chmod(mnemonic_file_path, stat.S_IREAD)
    if not credentials.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError(load_text(['err_verify_keystores']))
    if not verify_deposit_data_json(deposits_file, credentials.credentials):
        raise ValidationError(load_text(['err_verify_deposit']))
    click.echo(load_text(['msg_creation_success']) + folder)
    #click.pause(load_text(['msg_pause']))
