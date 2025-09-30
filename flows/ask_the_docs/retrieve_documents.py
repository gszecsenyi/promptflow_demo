"""
Retrieve relevant documents from the vector database based on the question.
"""
import os
import sys

# Try to import promptflow, but make it optional for standalone use
try:
    from promptflow import tool
except ImportError:
    # Define a dummy decorator for standalone use
    def tool(func):
        return func

# Add parent directory to path to import vectordb
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from vectordb import VectorDB
import numpy as np


def get_simple_embedding(text: str, dimension: int = 384) -> list:
    """
    Generate a simple embedding for text using character-based hashing.
    In production, this would use a proper embedding model like sentence-transformers.
    
    Args:
        text: The text to embed
        dimension: The dimension of the output vector
        
    Returns:
        A list representing the embedding vector
    """
    # Simple deterministic embedding based on text
    np.random.seed(hash(text.lower()) % (2**32))
    embedding = np.random.randn(dimension)
    # Normalize the vector
    embedding = embedding / np.linalg.norm(embedding)
    return embedding.tolist()


def load_documents():
    """Load documents from data directory and create embeddings."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    db = VectorDB(dimension=384)
    
    # Load all text files from data directory
    if os.path.exists(data_dir):
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(data_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split into paragraphs for better retrieval
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                
                for para in paragraphs:
                    embedding = get_simple_embedding(para)
                    db.add(embedding, {
                        'text': para,
                        'source': filename
                    })
    
    return db


# Initialize the vector database (in production, this would be cached or persisted)
_db = None


@tool
def retrieve_documents(question: str, top_k: int = 3) -> str:
    """
    Retrieve relevant document chunks based on the question.
    
    Args:
        question: The user's question
        top_k: Number of top documents to retrieve
        
    Returns:
        A formatted string with the retrieved documents
    """
    global _db
    
    # Load documents if not already loaded
    if _db is None:
        _db = load_documents()
    
    # Get embedding for the question
    question_embedding = get_simple_embedding(question)
    
    # Search for similar documents
    results = _db.search(question_embedding, top_k=top_k)
    
    # Format the results
    if not results:
        return "No relevant documents found."
    
    context_parts = []
    for i, (metadata, score) in enumerate(results, 1):
        context_parts.append(f"[Document {i}] (Source: {metadata['source']}, Score: {score:.3f})\n{metadata['text']}")
    
    return "\n\n".join(context_parts)
