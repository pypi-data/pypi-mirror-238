from inq.cli import main
from inq.utils.currency import CurrencyConverter


@main
def main(cmd: str) -> int:
    if match := CurrencyConverter.arg_pattern.match(cmd):
        converter = CurrencyConverter.from_match(match)
    else:
        raise ValueError("Unrecognized command")
    print(converter.run())
    return 0
