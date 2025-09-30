# Quick Start Guide

This guide will help you get started with the PromptFlow Ask-the-Docs demo in minutes.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gszecsenyi/promptflow_demo.git
cd promptflow_demo
```

2. Install basic dependencies:
```bash
pip install numpy
```

3. (Optional) Install PromptFlow for full functionality:
```bash
pip install -r requirements.txt
```

## Quick Demo

### Option 1: Run the Vector Database Example

Try the simple vector database example to understand how it works:

```bash
python example_vectordb.py
```

This will demonstrate:
- Creating a vector database
- Adding vectors with metadata
- Searching for similar vectors
- Saving and loading the database

### Option 2: Run the Document Retrieval Demo

Test the ask-the-docs functionality without LLM:

```bash
python run_demo.py
```

This will:
1. Show example questions and retrieved documents
2. Enter interactive mode where you can ask questions

Try questions like:
- "What is Python?"
- "How do machine learning algorithms work?"
- "Tell me about PromptFlow"

### Option 3: Run Tests

Verify everything works correctly:

```bash
python test_demo.py
```

## Next Steps

### Add Your Own Documents

1. Create `.txt` files in the `data/` directory
2. Run the demo again - your documents will be automatically indexed

### Use with PromptFlow (Optional)

To use the complete LLM-powered flow:

1. Get an OpenAI API key from https://platform.openai.com/

2. Copy the connection template:
```bash
cp connection.yaml.example connection.yaml
```

3. Edit `connection.yaml` and add your API key

4. Create the connection in PromptFlow:
```bash
pf connection create --file connection.yaml --name open_ai_connection
```

5. Test the flow:
```bash
pf flow test --flow flows/ask_the_docs --inputs question="What is Python?"
```

6. Run interactively:
```bash
pf flow test --flow flows/ask_the_docs --interactive
```

## Understanding the Code

- **`vectordb.py`**: Simple in-memory vector database implementation
- **`flows/ask_the_docs/`**: PromptFlow flow definition
  - `flow.dag.yaml`: Flow structure and configuration
  - `retrieve_documents.py`: Document retrieval logic
  - `generate_answer.jinja2`: LLM prompt template
- **`data/`**: Sample documents for testing
- **`test_demo.py`**: Automated tests
- **`run_demo.py`**: Standalone demo without PromptFlow
- **`example_vectordb.py`**: Simple vectordb usage example

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'numpy'`
- Solution: Run `pip install numpy`

**Issue**: `ModuleNotFoundError: No module named 'promptflow'`
- Solution: The standalone demos (test_demo.py, run_demo.py) work without PromptFlow
- To use PromptFlow features: `pip install -r requirements.txt`

**Issue**: Document retrieval returns unexpected results
- Note: This demo uses simple hash-based embeddings for demonstration
- For better results, use real embedding models (see README.md)

## What's Next?

1. Add more documents to the `data/` directory
2. Modify the prompt template in `generate_answer.jinja2`
3. Adjust retrieval parameters (top_k) in `flow.dag.yaml`
4. Replace hash-based embeddings with real models like sentence-transformers

For more details, see the full README.md file.
