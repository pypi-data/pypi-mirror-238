import click
import nltk

from dotenv import load_dotenv
from commands import scrape, split

# Downloading punkt only when it's not present
nltk.download('punkt', quiet=True)

load_dotenv()


# CLI Main Group
@click.group()
def cli():
    """Wayble is the official CLI for Wayble AI"""
    pass


cli.add_command(scrape.scrape)
cli.add_command(split.split)

if __name__ == '__main__':
    cli()
