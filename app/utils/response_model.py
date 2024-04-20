from typing import List

from pydantic import BaseModel


class Document(BaseModel):
    filename: str
    content: str
    type: str
    project: str
    organisation_id: str
    embedding_id: str


class DocumentList(BaseModel):
    documents: List[Document]


class EmbeddingSearchResponse(BaseModel):
    filename: str
    score: str


class EmbeddingSearchResponseList(BaseModel):
    documents: List[EmbeddingSearchResponse]
