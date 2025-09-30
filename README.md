# PromptFlow Ask-the-Docs Demo

A demonstration project showcasing how to build a question-answering system using PromptFlow and an in-memory vector database. This project implements a simple RAG (Retrieval Augmented Generation) system that can answer questions based on a collection of documents.

## Features

- **In-Memory Vector Database**: Custom implementation of a vector database (`vectordb.py`) for document similarity search
- **Document Retrieval**: Semantic search to find relevant document chunks based on user questions
- **PromptFlow Integration**: Complete flow definition for ask-the-docs functionality
- **Sample Documents**: Includes test data covering Python, Machine Learning, PromptFlow, and Vector Databases
- **Standalone Testing**: Can test document retrieval without full PromptFlow setup

## Project Structure

```
promptflow_demo/
├── vectordb.py                      # In-memory vector database implementation
├── flows/
│   └── ask_the_docs/
│       ├── flow.dag.yaml            # PromptFlow flow definition
│       ├── retrieve_documents.py    # Document retrieval logic
│       └── generate_answer.jinja2   # LLM prompt template
├── data/                            # Sample documents
│   ├── python.txt
│   ├── machine_learning.txt
│   ├── promptflow.txt
│   └── vector_databases.txt
├── test_demo.py                     # Unit tests
├── run_demo.py                      # Standalone demo script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gszecsenyi/promptflow_demo.git
cd promptflow_demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Standalone Demo

To test the document retrieval functionality without PromptFlow:

```bash
python run_demo.py
```

This will:
1. Show sample questions and retrieved documents
2. Enter interactive mode where you can ask your own questions

### Running Tests

To run the test suite:

```bash
python test_demo.py
```

### Using with PromptFlow

To run the complete flow with PromptFlow (requires OpenAI API key):

1. Set up your OpenAI connection in PromptFlow:
```bash
pf connection create --file connection.yaml --name open_ai_connection
```

2. Test the flow:
```bash
pf flow test --flow flows/ask_the_docs --inputs question="What is Python?"
```

3. Run the flow interactively:
```bash
pf flow test --flow flows/ask_the_docs --interactive
```

## How It Works

### Vector Database (`vectordb.py`)

The `VectorDB` class provides:
- Storage of high-dimensional vectors with metadata
- Cosine similarity-based search
- Batch operations for efficiency
- Save/load functionality for persistence

Key methods:
- `add(vector, metadata)`: Add a document vector
- `search(query_vector, top_k)`: Find similar documents
- `save(filepath)` / `load(filepath)`: Persist the database

### Document Retrieval (`retrieve_documents.py`)

The retrieval process:
1. Loads documents from the `data/` directory
2. Splits documents into paragraphs for better granularity
3. Generates embeddings for each paragraph (using simple hash-based embedding for demo)
4. Stores embeddings in the vector database
5. For queries, generates an embedding and finds the most similar documents

**Note**: This demo uses a simple hash-based embedding for demonstration purposes. In production, you should use proper embedding models like:
- `sentence-transformers` (e.g., `all-MiniLM-L6-v2`)
- OpenAI's `text-embedding-ada-002`
- Azure OpenAI embeddings

### PromptFlow Flow

The flow consists of two main nodes:

1. **retrieve_documents**: Python node that searches the vector database
2. **generate_answer**: LLM node that generates a response based on retrieved context

## Adding Your Own Documents

To add your own documents:

1. Create text files in the `data/` directory
2. Each file will be automatically loaded and indexed
3. Documents are split into paragraphs for better retrieval granularity

## Customization

### Using Real Embeddings

To use proper embeddings, modify `retrieve_documents.py`:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list:
    return model.encode(text).tolist()
```

### Adjusting Retrieval

Modify the `top_k` parameter in `flow.dag.yaml` or when calling `retrieve_documents()` to change the number of retrieved documents.

### Changing LLM Parameters

Edit `flow.dag.yaml` to adjust:
- `temperature`: Controls randomness (0.0 to 1.0)
- `max_tokens`: Maximum response length
- `deployment_name`: LLM model to use

## Example Questions

Try asking questions like:
- "What is Python used for?"
- "Explain the types of machine learning"
- "What are the key features of PromptFlow?"
- "How do vector databases work?"
- "What is reinforcement learning?"

## Dependencies

- `promptflow`: Core PromptFlow library
- `numpy`: Numerical operations for vector database
- `openai`: OpenAI API client (for LLM integration)

## License

This is a demonstration project for educational purposes.

## Contributing

Feel free to submit issues or pull requests to improve the demo!

## Notes

- This implementation uses a simple in-memory vector database suitable for small-scale demos
- For production use, consider dedicated vector databases like Pinecone, Weaviate, or Qdrant
- The embedding generation uses a simple hash-based approach for demo purposes
- In production, use proper embedding models for better retrieval quality