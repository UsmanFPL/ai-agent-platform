"""
Vector store configuration for embeddings and RAG
"""
import os
import chromadb
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


class VectorStoreManager:
    """Manages vector store operations for the AI Agent Platform"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
    
    def get_collection(self, collection_name: str):
        """Get or create a Chroma collection"""
        return Chroma(
            client=self.chroma_client,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
    
    def add_documents(self, collection_name: str, documents: list, metadatas: list = None):
        """Add documents to a collection"""
        collection = self.get_collection(collection_name)
        collection.add_documents(documents, metadatas=metadatas)
    
    def search(self, collection_name: str, query: str, k: int = 5):
        """Search for similar documents"""
        collection = self.get_collection(collection_name)
        return collection.similarity_search(query, k=k)
    
    def delete_collection(self, collection_name: str):
        """Delete a collection"""
        try:
            self.chroma_client.delete_collection(collection_name)
        except Exception:
            pass  # Collection might not exist


# Global vector store instance
vector_store = VectorStoreManager()