from typing import (
    List,
    Optional,
)

from stc_geck.advices import BaseDocumentHolder
from stc_geck.client import StcGeck

from .base import (
    BaseDataSource,
    SourceDocument,
)


class GeckDataSource(BaseDataSource):
    def __init__(self, geck: StcGeck):
        self.geck = geck

    async def search_documents(
        self,
        query: str,
        limit: int = 5,
        sources: Optional[List[str]] = None
    ) -> List[SourceDocument]:
        documents = await self.geck.get_summa_client().search_documents({
            'index_alias': self.geck.index_alias,
            'query': {'boolean': {'subqueries': [
                {'occur': 'must', 'query': {'match': {'value': query.lower()}}},
                {'occur': 'must', 'query': {'term': {'field': 'languages', 'value': 'en'}}},
                {'occur': 'must', 'query': {'boolean': {'subqueries': [
                    {'occur': 'should', 'query': {'term': {'field': 'type', 'value': 'book'}}},
                    {'occur': 'should', 'query': {'term': {'field': 'type', 'value': 'edited-book'}}},
                    {'occur': 'should', 'query': {'term': {'field': 'type', 'value': 'monograph'}}},
                    {'occur': 'should', 'query': {'term': {'field': 'type', 'value': 'reference-book'}}},
                    {'occur': 'should', 'query': {'term': {'field': 'type', 'value': 'journal-article'}}},
                    {'occur': 'should', 'query': {'term': {'field': 'type', 'value': 'wiki'}}},
                ]}}},
            ]}},
            'collectors': [{'top_docs': {'limit': limit}}],
            'is_fieldnorms_scoring_enabled': False,
        })
        source_documents = []
        for document in documents:
            document_holder = BaseDocumentHolder(document)
            document_id = document_holder.get_internal_id()
            if not document_id:
                continue
            source_documents.append(SourceDocument(
                document=document,
                document_id=document_id,
            ))
        return source_documents
