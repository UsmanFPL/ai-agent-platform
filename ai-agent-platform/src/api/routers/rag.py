from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, Any, List, Optional
from ...core.rag import rag_manager
from langchain.schema import Document

router = APIRouter()

@router.post("/documents")
async def add_documents(
    texts: List[str],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    collection_name: Optional[str] = None
):
    """Add text documents to the RAG system"""
    try:
        documents = []
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            documents.append(Document(page_content=text, metadata=metadata))
        
        result = await rag_manager.add_documents(documents, collection_name)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add documents: {str(e)}")

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    collection_name: Optional[str] = None
):
    """Upload and process a file for RAG"""
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the file
        result = await rag_manager.load_file(temp_path, collection_name)
        
        # Clean up temp file
        import os
        os.remove(temp_path)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@router.get("/search")
async def search_documents(
    query: str,
    k: int = 5,
    collection_filter: Optional[str] = None
):
    """Search for relevant documents"""
    try:
        results = await rag_manager.search(query, k, collection_filter)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/context")
async def get_context(
    query: str,
    max_tokens: int = 2000
):
    """Get relevant context for a query"""
    try:
        context = await rag_manager.get_context(query, max_tokens)
        return {
            "query": query,
            "context": context,
            "token_estimate": len(context) // 4
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get context: {str(e)}")

@router.get("/stats")
async def get_stats():
    """Get RAG system statistics"""
    try:
        stats = rag_manager.get_collection_stats()
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@router.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """Delete a document collection"""
    try:
        result = await rag_manager.delete_collection(collection_name)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete collection: {str(e)}")

@router.get("/health")
async def rag_health():
    """Check RAG system health"""
    try:
        stats = rag_manager.get_collection_stats()
        return {
            "status": "healthy",
            "vectorstore_initialized": rag_manager.vectorstore is not None,
            "stats": stats
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }