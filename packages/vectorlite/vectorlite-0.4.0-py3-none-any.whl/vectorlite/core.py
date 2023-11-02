import os
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch
from hnswlib import Index
from pydantic import BaseModel, Field
from langchain.schema.retriever import BaseRetriever
from typing import List

class Document(BaseModel):
    page_content: str
    metadata: dict

class DocumentList(BaseModel):
    documents: List[Document]

class VectorLite:
    def __init__(self, embedder=None):
        self.db = []

        if embedder:
            self.embedder = embedder
        else:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.index_file = "vectorlite_index.bin"
        if os.path.exists(self.index_file):
            self.index = joblib.load(self.index_file)
        else:
            self.index = None
        
        self.bin_file = "vectorlite_data.bin"
        if os.path.exists(self.bin_file):
            self.db = joblib.load(self.bin_file)
        else:
            joblib.dump(self.db, self.bin_file)

    def _save_index_to_bin(self):
        joblib.dump(self.index, self.index_file)

    def _save_db_to_bin(self):
        joblib.dump(self.db, self.bin_file)

    def _initialize_index(self, data_size):
        if data_size < 1000:
            ef_construction, M = 100, 8
        elif data_size < 10000:
            ef_construction, M = 200, 16
        else:
            ef_construction, M = 400, 32
        
        dim = self.embedder.get_sentence_embedding_dimension()
        self.index = Index(space='cosine', dim=dim)
        self.index.init_index(max_elements=1000000, ef_construction=ef_construction, M=M)
        self._save_index_to_bin()

    def create(self, data):
        page_contents = [doc.page_content for doc in data]
        embeddings = self.embedder.encode(page_contents)
        if not self.index:
            self._initialize_index(len(data))
        for idx, doc in enumerate(data):
            self.db.append({
                'page_content': doc.page_content,
                'metadata': doc.metadata
            })
            self.index.add_items(embeddings[idx], idx)
        self._save_index_to_bin()
        self._save_db_to_bin()

    def read_all(self, max_items=None):
        data_subset = self.db[:max_items] if max_items else self.db
        return [Document(**doc) for doc in data_subset]

    def read(self, idx):
        return Document(**self.db[idx])

    def update(self, idx, new_data):
        self.db[idx] = new_data
        new_embedding = self.embedder.encode(new_data)
        self.index.add_items(new_embedding, idx)
        self._save_index_to_bin()
        self._save_db_to_bin()

    def delete(self, idx):
        del self.db[idx]
        self._save_index_to_bin()
        self._save_db_to_bin()

    def similarity_search(self, query, k=5):
        query_embedding = self.embedder.encode([query])
        k_val = min(k, len(self.db))
        labels, distances = self.index.knn_query(query_embedding, k=k_val)
        return [Document(**self.db[idx.item()]) for idx in labels[0]]

    def semantic_search(self, query, k=5):
        query_embedding = self.embedder.encode([query], convert_to_tensor=True)
        page_contents = [doc['page_content'] for doc in self.db]
        cos_scores = util.pytorch_cos_sim(query_embedding, torch.tensor(self.embedder.encode(page_contents)))
        k_val = min(k, len(self.db))
        top_results = torch.topk(cos_scores.squeeze(), k=k_val)
        indices = top_results.indices.squeeze().tolist()
        return [Document(**self.db[idx]) for idx in indices]
    
    @classmethod
    def from_documents(cls, documents, embedder=None):
        vl = cls(embedder=embedder)
        vl.create(documents)
        return vl

    def as_retriever(self):
        return VectorLiteRetriever(self)

class VectorLiteRetriever(BaseRetriever):
    vectorlite: VectorLite = Field(..., description="The VectorLite instance")

    def __init__(self, vectorlite):
        self.vectorlite = vectorlite
        super().__init__()

    def _get_relevant_documents(self, query, k=5):
        # Use semantic search to get the relevant documents
        relevant_docs_indices = self.vectorlite.semantic_search(query, k)
        # Convert to Document format
        relevant_documents = [self.vectorlite.read(idx) for idx in relevant_docs_indices]
        # Return the relevant documents along with their indices
        return [(idx, doc) for idx, doc in zip(relevant_docs_indices, relevant_documents)]

    def as_retriever(self):
        return {
            'object': self,
            'index': self.vectorlite.index,
            'pipeline': self.vectorlite.embedder
        }

