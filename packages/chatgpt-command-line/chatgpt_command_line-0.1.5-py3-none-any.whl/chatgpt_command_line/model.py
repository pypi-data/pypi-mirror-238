from __future__ import annotations

import os
from typing import Dict, List, Literal, TypeAlias, Union
from uuid import uuid4

import openai
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from requests import post

Vector: TypeAlias = List[float]
Value: TypeAlias = str | int | float | bool | List[str]
MetaData: TypeAlias = Dict[str, Value]
Filter: TypeAlias = Literal["$eq", "$ne", "$lt", "$lte", "$gt", "$gte", "$in", "$nin"]
AndOr: TypeAlias = Literal["$and", "$or"]
Query: TypeAlias = Union[
	Dict[str, Union[Value, "Query", List[Value], List["Query"]]],
	Dict[AndOr, List[Dict[str, Union[Value, "Query", List[Value], List["Query"]]]]],
]
Size = Literal["256x256", "512x512", "1024x1024"]
Format = Literal["url", "b64_json"]

class Embedding(BaseModel):
	id:str = Field(default_factory=lambda: str(uuid4()))	
	values: Vector
	metadata:MetaData

class UpsertRequest(BaseModel):
	vectors: List[Embedding]

class UpsertResponse(BaseModel):
	upsertedCount: int

class QueryRequest(BaseModel):
	"""Request to query for similar vectors."""

	topK: int = Field(default=10)
	filter: dict[str,Value] = Field(...)
	includeMetadata: bool = Field(default=True)
	vector: Vector = Field(...)
	
class QueryMatch(BaseModel):
	"""A single match from a query."""

	id: str = Field(...)
	score: float = Field(...)
	metadata: MetaData = Field(...)
	
class QueryResponse(BaseModel):
	"""Response to a query."""

	matches: List[QueryMatch] = Field(...)

class APIClient(BaseModel):
	base_url: str = Field(...)
	headers: dict[str, str] = Field(...)
	

class PineconeClient(APIClient):
	base_url: str = Field(default=os.environ.get("PINECONE_API_URL", "https://api.pinecone.io")) # type: ignore
	headers: dict[str, str] = Field(default_factory=lambda: {"api-key": os.environ.get("PINECONE_API_KEY","")}) # type: ignore
	
	def upsert(self, texts: List[str]) -> int:
		"""Upsert embeddings into Pinecone."""
		vectors = [Embedding(values=self.create_vector([text])[0],metadata={"text":text}) for text in texts]
		response = post(f"{self.base_url}/vectors/upsert", json=UpsertRequest(vectors=vectors).dict(), headers=self.headers,timeout=120)
		response.raise_for_status()
		return UpsertResponse(**response.json()).upsertedCount
			
	def create_vector(self,input:list[str])->List[Vector]:
		return [r.embedding for r in openai.Embedding.create(input=input,model="text-embedding-ada-002").data] # type: ignore

	def query(self, text:str) -> str:
		"""Query Pinecone for similar vectors."""
		vector = self.create_vector([text])[0]
		query = QueryRequest(vector=vector, filter={}, topK=5, includeMetadata=True)
		response = post(f"{self.base_url}/query", json=query.dict(), headers=self.headers,timeout=10)
		response.raise_for_status()
		matches = QueryResponse(**response.json()).matches
		search_results = "\n".join(f"Score:{match.score * 100:.2f}%: {match.metadata.get('text','')}" for match in matches)
		return f"Similar results in the knowledge base: \n{search_results}"

	
