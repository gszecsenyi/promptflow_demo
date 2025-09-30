"""
Standalone demo script for ask-the-docs functionality.
This can be run without PromptFlow to test the document retrieval.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from flows.ask_the_docs.retrieve_documents import retrieve_documents


def main():
    """Run the ask-the-docs demo."""
    print("="*60)
    print("Ask-the-Docs Demo (Document Retrieval)")
    print("="*60)
    print()
    
    # Sample questions to demonstrate
    questions = [
        "What is Python used for?",
        "Explain machine learning types",
        "What are the key features of PromptFlow?",
        "How do vector databases work?",
        "What is reinforcement learning?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 60)
        
        # Retrieve documents
        context = retrieve_documents(question, top_k=2)
        print(context)
        print()
    
    # Interactive mode
    print("\n" + "="*60)
    print("Interactive Mode (type 'quit' to exit)")
    print("="*60)
    
    while True:
        try:
            question = input("\nYour question: ").strip()
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not question:
                continue
            
            print()
            context = retrieve_documents(question, top_k=3)
            print(context)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
