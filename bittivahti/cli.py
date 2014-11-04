import click

from .bittivahti import loop


@click.command('bittivahti')
@click.option('-c', '--colors', help='Show something with colors',
              is_flag=True)
@click.option('-i', '--interval', default=3, type=click.FLOAT,
              help='Wait SECONDS between updates', metavar='SECONDS')
def main(interval, colors):
    """Display traffic statistics on local network interfaces"""
    dynunit = False
    loop(interval, dynunit, colors)
