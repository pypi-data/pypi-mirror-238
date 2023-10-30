import click
import base64
from getpass import getpass

def get_code_parts_from_keyboard():
    try:
        first_key_part = base64.b64decode(getpass("Enter first key part: "))

        key_id = first_key_part[0] - 1
        total_keys = first_key_part[1]
        key_part = first_key_part[2:]
        collected_key_parts = [None] * total_keys
        collected_key_parts[key_id] = key_part

        while total_keys - sum(x is not None for x in collected_key_parts) > 0:
            next_code = base64.b64decode(getpass(
                f"{total_keys - sum(x is not None for x in collected_key_parts)} keys remaning. Enter key: "
            ))

            key_id = next_code[0] - 1
            key_part = next_code[2:]
            collected_key_parts[key_id] = key_part

    except KeyboardInterrupt:
        return

    click.echo("".join([x.decode() for x in collected_key_parts]))
