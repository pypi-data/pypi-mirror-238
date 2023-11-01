import click

from typing import TypedDict
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from lib.jsonio import jsonio


class InputParams(TypedDict):
    input_file: str
    chunk_size: int
    overlap_size: int


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.argument('output_file', type=click.Path(writable=True))
@jsonio
def split(params: InputParams) -> list:
    """
    Splits text from text files into chunks and writes the result to the output file in JSON format.

    [INPUT_FILE] is the path to a JSON file with the input params.\n
    👉 { input_file: str, chunk_size: int(256), overlap_size: int(128) }

    [OUTPUT_FILE] is the path to the file to which the chunks will be saved.
    """
    loader = TextLoader(params['input_file'])
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_overlap=params.get('overlap_size', 128),
        chunk_size=params.get('chunk_size', 512)
    )

    # Split the documents into chunks
    docs = text_splitter.split_documents(documents)

    # Extract page content from each document
    return [doc.page_content for doc in docs]
