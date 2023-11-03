import functools
import json
import logging
import re
import sys
import textwrap
from typing import Optional

import fire
from termcolor import colored

from .cybrex_ai import CybrexAI
from .exceptions import QdrantStorageNotAvailableError


def exception_handler(func):
    @functools.wraps(func)
    async def wrapper_func(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except QdrantStorageNotAvailableError as e:
            print(
                f"{colored('INFO', 'red')}: Cannot connect to Qdrant: {e.info}\n"
                f"{colored('HINT', 'yellow')}: Launch qdrant using `docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant`",
                file=sys.stderr,
            )
            raise
    return wrapper_func


class CybrexCli:
    def __init__(self, cybrex: Optional[CybrexAI] = None):
        self.cybrex = cybrex or CybrexAI()

    async def add_all_documents(self):
        async with self.cybrex as cybrex:
            async for document in cybrex.geck.get_summa_client().documents('nexus_science'):
                document = json.loads(document)
                await self.cybrex.upsert_documents([document])

    @exception_handler
    async def chat_doc(self, document_query: str, query: str, n_chunks: int = 5, minimum_score: float = 0.5):
        """
        Ask a question about content of document identified by DOI.

        :param document_query: query that returns unique document
        :param query: Text query to the document
        :param n_chunks: the number of chunks to extract
            more means more tokens to use and more precision in answer
        """
        async with self.cybrex as cybrex:
            print(f"{colored('Document', 'green')}: {document_query}")
            print(f"{colored('Q', 'green')}: {query}")
            cybrex_response = await cybrex.chat_document(
                document_query,
                query,
                n_chunks,
                minimum_score=minimum_score,
            )
            print(f"{colored('A', 'green')}: {cybrex_response.answer}")

    @exception_handler
    async def chat_sci(
        self,
        query: str,
        n_chunks: int = 5,
        n_documents: int = 10,
        minimum_score: float = 0.5,
    ):
        """
        Ask a general questions

        :param query: text query to the document
        :param n_chunks: the number of chunks to extract
            more means more tokens to use and more precision in answer
        :param n_documents: the number of chunks to extract
            more means more tokens to use and more precision in answer
        :param minimum_score:
        """
        async with self.cybrex as cybrex:
            print(f"{colored('Q', 'green')}: {query}")
            cybrex_response = await cybrex.chat_science(
                query=query,
                n_chunks=n_chunks,
                n_documents=n_documents,
                minimum_score=minimum_score,
            )
            answer = re.sub(r'\(DOI:\s*([^)]+)\)', r'(https://doi.org/\g<1>)', cybrex_response.answer)
            references = []
            visited = set()
            for chunk in cybrex_response.chunks:
                field, value = chunk.document_id.split(':', 1)
                document_id = f'{field}:{value}'
                if document_id in visited:
                    continue
                visited.add(document_id)
                references.append(f'{document_id}: {chunk.title}')
            references = '\n'.join(references)
            print(f"{colored('A', 'green')}: {answer}")
            print(f"{colored('References', 'green')}:\n{textwrap.indent(references, ' - ')}")

    @exception_handler
    async def sum_doc(self, document_query: str):
        """
        Summarization of the document

        :param document_query: query that returns unique document
        """
        async with self.cybrex as cybrex:
            print(f"{colored('Document', 'green')}: {document_query}")
            cybrex_response = await cybrex.summarize_document(document_query)
            print(f"{colored('Summarization', 'green')}: {cybrex_response.answer}")

    @exception_handler
    async def semantic_search(
        self,
        query: str,
        n_chunks: int = 5,
        n_documents: int = 10,
        minimum_score: float = 0.5,
        use_only_keywords: bool = True,
    ):
        """
        Search related to query text chunks among `n` documents

        :param query: query to STC
        :param n_chunks: number of chunks to return
        :param n_documents: the number of documents to extract from STC
        :param minimum_score:
        :param use_only_keywords:
        """
        async with self.cybrex as cybrex:
            print(f"{colored('Q', 'green')}: {query}")
            scored_chunks = await cybrex.semantic_search(
                query=query,
                n_chunks=n_chunks,
                n_documents=n_documents,
                minimum_score=minimum_score,
                use_only_keywords=use_only_keywords,
            )
            references = []
            for scored_chunk in scored_chunks:
                field, value = scored_chunk.chunk.document_id.split(':', 1)
                document_id = f'{field}:{value}'
                title = scored_chunk.chunk.title.replace('\n', ' - ')
                references.append(f' - {document_id}: {title}\n   {scored_chunk.chunk.text}')
            references = '\n'.join(references)
            print(f"{colored('References', 'green')}:\n{references}")


def cybrex_cli(debug: bool = False):
    """
    :param debug: add debugging output
    :return:
    """
    logging.basicConfig(stream=sys.stdout, level=logging.INFO if debug else logging.ERROR)
    cybrex = CybrexCli()
    return {
        'add-all-chunks': cybrex.add_all_documents,
        'chat-doc': cybrex.chat_doc,
        'chat-sci': cybrex.chat_sci,
        'semantic-search': cybrex.semantic_search,
        'sum-doc': cybrex.sum_doc,
        'write-config': cybrex.cybrex.ensure_config,
    }


def main():
    fire.Fire(cybrex_cli, name='cybrex')


if __name__ == '__main__':
    main()
