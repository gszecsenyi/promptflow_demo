"""
Simple in-memory vector database for document similarity search.
This module provides a basic implementation of a vector database that stores
document embeddings and performs similarity searches.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
import json


class VectorDB:
    """
    In-memory vector database for storing and searching document embeddings.
    """
    
    def __init__(self, dimension: int = 1536):
        """
        Initialize the vector database.
        
        Args:
            dimension: The dimension of the embedding vectors (default: 1536 for OpenAI embeddings)
        """
        self.dimension = dimension
        self.vectors: List[np.ndarray] = []
        self.metadata: List[Dict] = []
        
    def add(self, vector: List[float], metadata: Dict) -> None:
        """
        Add a vector with associated metadata to the database.
        
        Args:
            vector: The embedding vector as a list of floats
            metadata: Dictionary containing document metadata (e.g., text, source)
        """
        if len(vector) != self.dimension:
            raise ValueError(f"Vector dimension {len(vector)} does not match database dimension {self.dimension}")
        
        self.vectors.append(np.array(vector))
        self.metadata.append(metadata)
        
    def add_batch(self, vectors: List[List[float]], metadata_list: List[Dict]) -> None:
        """
        Add multiple vectors with their metadata to the database.
        
        Args:
            vectors: List of embedding vectors
            metadata_list: List of metadata dictionaries
        """
        if len(vectors) != len(metadata_list):
            raise ValueError("Number of vectors must match number of metadata entries")
        
        for vector, metadata in zip(vectors, metadata_list):
            self.add(vector, metadata)
            
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for the most similar vectors to the query vector.
        
        Args:
            query_vector: The query embedding vector
            top_k: Number of top results to return
            
        Returns:
            List of tuples containing (metadata, similarity_score)
        """
        if len(self.vectors) == 0:
            return []
        
        if len(query_vector) != self.dimension:
            raise ValueError(f"Query vector dimension {len(query_vector)} does not match database dimension {self.dimension}")
        
        query_vec = np.array(query_vector)
        
        # Calculate cosine similarity
        similarities = []
        for vec in self.vectors:
            similarity = self._cosine_similarity(query_vec, vec)
            similarities.append(similarity)
        
        # Get top k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return results with metadata and scores
        results = [(self.metadata[i], similarities[i]) for i in top_indices]
        return results
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def save(self, filepath: str) -> None:
        """
        Save the database to a file.
        
        Args:
            filepath: Path to save the database
        """
        data = {
            'dimension': self.dimension,
            'vectors': [vec.tolist() for vec in self.vectors],
            'metadata': self.metadata
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
    
    def load(self, filepath: str) -> None:
        """
        Load the database from a file.
        
        Args:
            filepath: Path to load the database from
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.dimension = data['dimension']
        self.vectors = [np.array(vec) for vec in data['vectors']]
        self.metadata = data['metadata']
    
    def clear(self) -> None:
        """Clear all vectors and metadata from the database."""
        self.vectors = []
        self.metadata = []
    
    def __len__(self) -> int:
        """Return the number of vectors in the database."""
        return len(self.vectors)
