import click
from de_toolkit.vm import start,stop,connect,test

@click.group()
def cli():
    pass

cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)
cli.add_command(test)

if __name__ == '__main__':
    cli()
