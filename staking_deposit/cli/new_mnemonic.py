import click
from typing import (
    Any,
)

from staking_deposit.key_handling.key_derivation.mnemonic import (
    get_mnemonic,
    reconstruct_mnemonic,
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
    help=load_text(['arg_new_mnemonic', 'help'], func='new_mnemonic'),
)
@click.pass_context
@generate_keys_arguments_decorator
@click.option('--save_mnemonic', is_flag=True, help='Skip mnemonic verification if set')
def new_mnemonic(ctx: click.Context, save_mnemonic: bool, **kwargs: Any) -> None:
    mnemonic_language = 'english'  # Hardcode language to english
    mnemonic = get_mnemonic(language=mnemonic_language, words_path=WORD_LISTS_PATH)
    if not save_mnemonic:
        test_mnemonic = ''
        while mnemonic != reconstruct_mnemonic(test_mnemonic, WORD_LISTS_PATH):
            click.clear()
            click.echo(load_text(['msg_mnemonic_presentation']))
            click.echo('\n\n%s\n\n' % mnemonic)
            click.pause(load_text(['msg_press_any_key']))

            click.clear()
            test_mnemonic = click.prompt(load_text(['msg_mnemonic_retype_prompt']) + '\n\n')
    click.clear()
    # Do NOT use mnemonic_password.
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': ''}
    ctx.params['validator_start_index'] = 0
    ctx.params['save_mnemonic'] = save_mnemonic  # Add save_mnemonic to ctx.params
    ctx.forward(generate_keys)
