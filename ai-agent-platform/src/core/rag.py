from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, PDFLoader, CSVLoader
from langchain.schema import Document
from typing import List, Dict, Any, Optional
import os
import chromadb

class RAGManager:
    """Retrieval-Augmented Generation manager"""
    
    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize the vector store"""
        try:
            # Create Chroma client
            client = chromadb.PersistentClient(path=self.persist_directory)
            
            # Initialize Chroma vectorstore
            self.vectorstore = Chroma(
                client=client,
                collection_name="ai_agent_knowledge",
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            
        except Exception as e:
            print(f"Failed to initialize vectorstore: {e}")
            # Fallback to in-memory store
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                collection_name="ai_agent_knowledge"
            )
    
    async def add_documents(self, documents: List[Document], collection_name: str = None) -> Dict[str, Any]:
        """Add documents to the vector store"""
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add metadata for collection if specified
            if collection_name:
                for chunk in chunks:
                    chunk.metadata["collection"] = collection_name
            
            # Add to vectorstore
            ids = self.vectorstore.add_documents(chunks)
            
            return {
                "success": True,
                "documents_added": len(documents),
                "chunks_created": len(chunks),
                "ids": ids
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def add_text(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Add raw text to the vector store"""
        document = Document(page_content=text, metadata=metadata or {})
        return await self.add_documents([document])
    
    async def load_file(self, file_path: str, collection_name: str = None) -> Dict[str, Any]:
        """Load and add a file to the vector store"""
        try:
            # Determine file type and use appropriate loader
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                loader = TextLoader(file_path)
            elif file_extension == '.pdf':
                loader = PDFLoader(file_path)
            elif file_extension == '.csv':
                loader = CSVLoader(file_path)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_extension}"
                }
            
            # Load documents
            documents = loader.load()
            
            # Add filename to metadata
            for doc in documents:
                doc.metadata["source_file"] = os.path.basename(file_path)
                doc.metadata["file_path"] = file_path
            
            # Add to vectorstore
            result = await self.add_documents(documents, collection_name)
            result["file_path"] = file_path
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    async def search(self, query: str, k: int = 5, collection_filter: str = None) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        try:
            # Build filter if collection specified
            filter_dict = None
            if collection_filter:
                filter_dict = {"collection": collection_filter}
            
            # Perform similarity search
            if filter_dict:
                results = self.vectorstore.similarity_search_with_score(
                    query, k=k, filter=filter_dict
                )
            else:
                results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": score
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    async def get_context(self, query: str, max_tokens: int = 2000) -> str:
        """Get relevant context for a query, limited by token count"""
        results = await self.search(query, k=10)
        
        context_parts = []
        current_tokens = 0
        
        for result in results:
            content = result["content"]
            # Rough token estimation (1 token ≈ 4 characters)
            content_tokens = len(content) // 4
            
            if current_tokens + content_tokens > max_tokens:
                break
            
            context_parts.append(content)
            current_tokens += content_tokens
        
        return "\n\n".join(context_parts)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            # Get collection info
            collection = self.vectorstore._collection
            count = collection.count()
            
            return {
                "total_documents": count,
                "collection_name": collection.name,
                "persist_directory": self.persist_directory
            }
            
        except Exception as e:
            return {
                "error": str(e)
            }
    
    async def delete_collection(self, collection_name: str) -> Dict[str, Any]:
        """Delete documents from a specific collection"""
        try:
            # Delete documents with matching collection metadata
            self.vectorstore.delete(where={"collection": collection_name})
            
            return {
                "success": True,
                "collection_deleted": collection_name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Global RAG manager instance
rag_manager = RAGManager()