# Using the Flow with PromptFlow

This document explains how to use the ask-the-docs flow with PromptFlow once you have it set up.

## Setup

1. Install PromptFlow:
```bash
pip install -r requirements.txt
```

2. Configure OpenAI connection:
```bash
# Copy the example configuration
cp connection.yaml.example connection.yaml

# Edit connection.yaml and add your OpenAI API key
# Then create the connection
pf connection create --file connection.yaml --name open_ai_connection
```

## Running the Flow

### Test with a Single Question

```bash
pf flow test --flow flows/ask_the_docs --inputs question="What is Python?"
```

Expected output:
```
{
  "answer": "Python is a high-level, interpreted programming language...",
  "context": "[Document 1] (Source: python.txt)..."
}
```

### Interactive Mode

```bash
pf flow test --flow flows/ask_the_docs --interactive
```

This opens an interactive session where you can ask multiple questions.

### Batch Testing

Create a test file `test_questions.jsonl`:
```jsonl
{"question": "What is Python?"}
{"question": "Explain machine learning types"}
{"question": "What is PromptFlow?"}
```

Run batch test:
```bash
pf run create --flow flows/ask_the_docs --data test_questions.jsonl --name ask_docs_test
```

View results:
```bash
pf run show --name ask_docs_test
pf run show-details --name ask_docs_test
```

### Evaluating the Flow

Create an evaluation flow to assess answer quality:

```bash
# View evaluation metrics
pf run show-metrics --name ask_docs_test
```

## Flow Architecture

The flow consists of two nodes:

### 1. retrieve_documents (Python Node)
- **Input**: User question
- **Process**: 
  1. Loads documents from the data directory
  2. Generates embeddings for document chunks
  3. Searches for the most similar chunks to the question
  4. Returns formatted context with source information
- **Output**: Retrieved document chunks as formatted text

### 2. generate_answer (LLM Node)
- **Input**: Question + Retrieved context
- **Process**: Uses GPT-3.5-turbo to generate an answer
- **Output**: Natural language answer based on the context

## Customizing the Flow

### Modify Retrieval Parameters

Edit `flow.dag.yaml` to change the number of retrieved documents:

```yaml
- name: retrieve_documents
  inputs:
    question: ${inputs.question}
    top_k: 5  # Change from 3 to 5
```

### Customize the Prompt

Edit `flows/ask_the_docs/generate_answer.jinja2`:

```jinja2
system:
You are an expert technical assistant specializing in AI and programming.
Answer questions based ONLY on the provided context.
If the answer is not in the context, say "I don't have that information."

user:
Context:
{{context}}

Question: {{question}}

Provide a detailed technical answer with examples if relevant.
```

### Change LLM Model

Edit `flow.dag.yaml`:

```yaml
- name: generate_answer
  inputs:
    deployment_name: gpt-4  # Change from gpt-3.5-turbo
    temperature: 0.5        # More deterministic
    max_tokens: 800         # Longer responses
```

### Add New Documents

Simply add `.txt` files to the `data/` directory:

```bash
echo "Your new document content" > data/my_topic.txt
```

The flow will automatically index new documents on the next run.

## Advanced Usage

### Using Real Embeddings

For better retrieval quality, modify `retrieve_documents.py` to use sentence-transformers:

```python
# Install: pip install sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_simple_embedding(text: str, dimension: int = 384) -> list:
    return model.encode(text).tolist()
```

### Persistent Vector Database

Save the vector database to avoid recomputing embeddings:

```python
# In retrieve_documents.py
import os

DB_PATH = 'vectordb.json'

if os.path.exists(DB_PATH):
    _db.load(DB_PATH)
else:
    _db = load_documents()
    _db.save(DB_PATH)
```

### Adding Metadata Filtering

Enhance search with metadata filters:

```python
def retrieve_documents(question: str, top_k: int = 3, source_filter: str = None):
    results = _db.search(question_embedding, top_k=top_k * 2)
    
    # Filter by source if specified
    if source_filter:
        results = [(m, s) for m, s in results if source_filter in m['source']]
    
    return format_results(results[:top_k])
```

## Deployment

### Local Serving

Serve the flow as a local endpoint:

```bash
pf flow serve --source flows/ask_the_docs --port 8080 --host localhost
```

Test the endpoint:
```bash
curl http://localhost:8080/score \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

### Build as Docker

Build the flow as a Docker container:

```bash
pf flow build --source flows/ask_the_docs --output dist --format docker
cd dist
docker build -t ask-the-docs .
docker run -p 8080:8080 ask-the-docs
```

## Monitoring and Debugging

### Enable Logging

```bash
# Set log level
export PF_LOGGING_LEVEL=DEBUG

pf flow test --flow flows/ask_the_docs --inputs question="Test"
```

### View Node Outputs

```bash
pf flow test --flow flows/ask_the_docs \
  --inputs question="Test" \
  --node retrieve_documents
```

### Trace Execution

View detailed execution trace:

```bash
pf run show-details --name <run_name> --verbose
```

## Best Practices

1. **Start Simple**: Test with small datasets before scaling
2. **Iterate on Prompts**: Experiment with different prompt templates
3. **Monitor Costs**: Track API usage and optimize token consumption
4. **Cache Embeddings**: Save vector database to avoid recomputing
5. **Version Control**: Keep flow definitions and data in version control
6. **Test Regularly**: Use batch testing to catch regressions

## Troubleshooting

**Issue**: "Connection 'open_ai_connection' not found"
- Run: `pf connection create --file connection.yaml --name open_ai_connection`

**Issue**: "Rate limit exceeded"
- Reduce batch size or add delays between requests
- Consider using a higher tier API key

**Issue**: Poor retrieval quality
- Use proper embedding models instead of hash-based embeddings
- Increase `top_k` to retrieve more context
- Split documents into smaller, more focused chunks

**Issue**: Answers not based on context
- Improve the prompt template to emphasize context usage
- Adjust temperature to make responses more deterministic
- Add examples to the prompt (few-shot learning)

For more help, see the [PromptFlow documentation](https://microsoft.github.io/promptflow/).
