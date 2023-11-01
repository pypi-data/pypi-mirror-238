import click
import requests

from lib.jsonio import jsonio
from typing import TypedDict
from bs4 import BeautifulSoup


class InputParams(TypedDict):
    url: str


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.argument('output_file', type=click.Path(writable=True))
@jsonio
def scrape(params: InputParams) -> str:
    """
    Scrapes text content from the specified URL and saves it to the output file.

    [INPUT_FILE] is the path to a JSON file with the input params.\n
    👉 { url: str }

    [OUTPUT_FILE] is the path to the file to which the scraped content will be saved.
    """
    try:
        response = requests.get(params.get('url'))
        response.raise_for_status()  # Ensure we got a successful response

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract and join text from the parsed HTML content
        text = " ".join(soup.stripped_strings)

        return {'content': text}

    except requests.RequestException as e:
        raise click.ClickException(f"Error extracting content from {params.get('url')}: {e}")
