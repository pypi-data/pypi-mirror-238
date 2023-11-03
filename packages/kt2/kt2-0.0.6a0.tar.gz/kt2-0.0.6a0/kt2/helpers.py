import click
from pyfiglet import Figlet
from wasabi import table

font = Figlet(font="slant")


def truncate(data, length=75):
    return (data[:length] + '...') if len(data) > length else data


def print_table(data, header, widths, bg_colors=None, aligns=("l", "l", "l")):
    formatted = table(
        data,
        header=header,
        widths=widths,
        aligns=aligns,
        bg_colors=bg_colors,
        divider=True,
    )
    click.secho(formatted)
