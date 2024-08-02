import click
import os
from typing import (
    Any,
)

from staking_deposit.key_handling.key_derivation.mnemonic import (
    get_mnemonic,
)
from staking_deposit.utils.click import (
    captive_prompt_callback,
    choice_prompt_func,
    jit_option,
)
from staking_deposit.utils.constants import (
    MNEMONIC_LANG_OPTIONS,
    WORD_LISTS_PATH,
)
from staking_deposit.utils.intl import (
    fuzzy_reverse_dict_lookup,
    load_text,
    get_first_options,
)

from .generate_keys import (
    generate_keys,
    generate_keys_arguments_decorator,
)

languages = get_first_options(MNEMONIC_LANG_OPTIONS)

@click.command(
    help=load_text(['arg_generate_mnemonic', 'help'], func='generate_mnemonic'),
)
@click.pass_context
@click.option('--mnemonic_path', type=str, help='Path to save the generated mnemonic')
def generate_mnemonic(ctx: click.Context, mnemonic_path: str, **kwargs: Any) -> str:
    print('\n***Using the tool on an offline and secure device is highly recommended to keep your mnemonic safe.***\n')
    mnemonic_language = 'english'  # Hardcode language to english
    mnemonic = get_mnemonic(language=mnemonic_language, words_path=WORD_LISTS_PATH)
    click.clear()
    if not mnemonic_path:
        click.echo(load_text(['msg_mnemonic_presentation']))
        click.echo('\n\n%s\n\n' % mnemonic)
        click.pause(load_text(['msg_press_any_key']))
    else:
        click.echo("This is your mnemonic (seed phrase). It is the ONLY way to retrieve your deposit.")
        click.echo('\n\n%s\n\n' % mnemonic)
        click.pause('The mnemonic will be save to %s. Press any key to continue...' % mnemonic_path)

    click.clear()
    # Do NOT use mnemonic_password.
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': ''}
    ctx.params['validator_start_index'] = 0
    ctx.params['mnemonic_path'] = mnemonic_path  # Add mnemonic_path to ctx.params

    if mnemonic_path:
        if os.path.exists(mnemonic_path):
            #with open(mnemonic_path, 'r') as file:
            #    existing_mnemonic = file.read().strip()
            #if existing_mnemonic:
            #    click.echo(f'The file {mnemonic_path} already contains exists. Please move {mnemonic_path} before saving a new one.')
            #    raise Exception(f'The file {mnemonic_path} already contains exists. Please move {mnemonic_path} before saving a new one.')
            if not os.access(mnemonic_path, os.W_OK):
                os.chmod(mnemonic_path, 0o666)  # Add write permission
        else:
            os.makedirs(os.path.dirname(mnemonic_path), exist_ok=True)

        with open(mnemonic_path, 'w') as file:
            file.write(mnemonic)
        with open(mnemonic_path, 'r') as file:
            written_content = file.read()
        if written_content != mnemonic:
            raise Exception(f'Failed to write mnemonic correctly to file, written_content {written_content} != {mnemonic}')
        os.chmod(mnemonic_path, 0o444)
        click.echo('The mnemonic has been saved to %s' % mnemonic_path)

    return mnemonic
