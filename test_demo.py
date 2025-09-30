"""
Test script for the ask-the-docs demo.
This script tests the vector database and document retrieval functionality.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from vectordb import VectorDB
import numpy as np


def test_vectordb():
    """Test basic VectorDB functionality."""
    print("Testing VectorDB...")
    
    # Create a database
    db = VectorDB(dimension=3)
    
    # Add some test vectors
    db.add([1.0, 0.0, 0.0], {'text': 'Document about X axis'})
    db.add([0.0, 1.0, 0.0], {'text': 'Document about Y axis'})
    db.add([0.0, 0.0, 1.0], {'text': 'Document about Z axis'})
    db.add([0.7, 0.7, 0.0], {'text': 'Document about XY plane'})
    
    print(f"Added {len(db)} documents to the database")
    
    # Test search
    query = [1.0, 0.1, 0.0]
    results = db.search(query, top_k=2)
    
    print("\nSearch results for query [1.0, 0.1, 0.0]:")
    for metadata, score in results:
        print(f"  - {metadata['text']} (score: {score:.3f})")
    
    # Verify the most similar is the X axis document
    assert results[0][0]['text'] == 'Document about X axis', "Top result should be X axis document"
    print("\n✓ VectorDB test passed!")
    

def test_document_loading():
    """Test loading and retrieving actual documents."""
    print("\n" + "="*60)
    print("Testing Document Loading and Retrieval...")
    
    # Import the retrieve function
    from flows.ask_the_docs.retrieve_documents import load_documents, get_simple_embedding
    
    # Load documents
    db = load_documents()
    print(f"Loaded {len(db)} document chunks")
    
    # Test retrieval with different questions
    test_questions = [
        "What is Python?",
        "Tell me about machine learning",
        "What is PromptFlow?",
        "How do vector databases work?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        embedding = get_simple_embedding(question)
        results = db.search(embedding, top_k=2)
        
        for i, (metadata, score) in enumerate(results, 1):
            print(f"  Result {i} (score: {score:.3f}, source: {metadata['source']}):")
            preview = metadata['text'][:100].replace('\n', ' ')
            print(f"    {preview}...")
    
    print("\n✓ Document loading and retrieval test passed!")


if __name__ == "__main__":
    try:
        test_vectordb()
        test_document_loading()
        print("\n" + "="*60)
        print("All tests passed! ✓")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
