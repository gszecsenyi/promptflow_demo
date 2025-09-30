"""
Example usage of the vectordb module.
This demonstrates how to use the VectorDB class for storing and searching vectors.
"""
from vectordb import VectorDB
import numpy as np


def main():
    print("VectorDB Example Usage")
    print("=" * 60)
    
    # Create a vector database with 3-dimensional vectors
    db = VectorDB(dimension=3)
    print(f"Created database with dimension: {db.dimension}")
    
    # Add some sample vectors with metadata
    print("\nAdding vectors to database...")
    db.add([1.0, 0.0, 0.0], {'category': 'red', 'description': 'Pure red color'})
    db.add([0.0, 1.0, 0.0], {'category': 'green', 'description': 'Pure green color'})
    db.add([0.0, 0.0, 1.0], {'category': 'blue', 'description': 'Pure blue color'})
    db.add([1.0, 1.0, 0.0], {'category': 'yellow', 'description': 'Mix of red and green'})
    db.add([1.0, 0.0, 1.0], {'category': 'magenta', 'description': 'Mix of red and blue'})
    db.add([0.0, 1.0, 1.0], {'category': 'cyan', 'description': 'Mix of green and blue'})
    
    print(f"Database now contains {len(db)} vectors")
    
    # Search for similar vectors
    print("\n" + "=" * 60)
    print("Search Examples")
    print("=" * 60)
    
    queries = [
        ([1.0, 0.5, 0.0], "Orange-ish (red + some green)"),
        ([0.5, 0.5, 1.0], "Light blue (blue + equal red/green)"),
        ([1.0, 0.0, 0.0], "Pure red")
    ]
    
    for query_vector, description in queries:
        print(f"\nQuery: {description}")
        print(f"Vector: {query_vector}")
        results = db.search(query_vector, top_k=3)
        print("Top 3 results:")
        for i, (metadata, score) in enumerate(results, 1):
            print(f"  {i}. {metadata['category']:10s} - {metadata['description']:30s} (similarity: {score:.3f})")
    
    # Demonstrate save and load
    print("\n" + "=" * 60)
    print("Save and Load Example")
    print("=" * 60)
    
    # Save to file
    db.save('/tmp/vectordb_example.json')
    print("✓ Database saved to /tmp/vectordb_example.json")
    
    # Create new database and load
    db2 = VectorDB()
    db2.load('/tmp/vectordb_example.json')
    print(f"✓ Database loaded - contains {len(db2)} vectors")
    
    # Verify it works
    results = db2.search([1.0, 0.0, 0.0], top_k=1)
    print(f"✓ Search test: Found '{results[0][0]['category']}' with similarity {results[0][1]:.3f}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
