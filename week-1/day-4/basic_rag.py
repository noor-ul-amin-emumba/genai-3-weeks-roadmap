from sentence_transformers import SentenceTransformer
import importlib
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Path Setup
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))

config = importlib.import_module("config")
call_llm = config.call_llm


# Initialize models globally
# Fast, lightweight embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Each element in the VECTOR_DB will be a tuple (chunk, embedding)
# The embedding is a list of floats, for example: [0.1, 0.04, -0.34, 0.21, ...]
VECTOR_DB = []


def add_chunk_to_database(chunk):
    embedding = embedding_model.encode(chunk)
    VECTOR_DB.append((chunk, embedding))


def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)


def retrieve(query, top_n=3):
    query_embedding = embedding_model.encode(query)
    # temporary list to store (chunk, similarity) pairs
    similarities = []
    for chunk, embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk, similarity))
    # sort by similarity in descending order, because higher similarity means more relevant chunks
    similarities.sort(key=lambda x: x[1], reverse=True)
    # finally, return the top N most relevant chunks
    return similarities[:top_n]


def main():
    # Load the dataset
    dataset_path = Path(__file__).parent / 'cat-facts.txt'

    dataset = []
    with open(dataset_path, 'r', encoding='utf-8') as file:
        dataset = file.readlines()
        print(f'Loaded {len(dataset)} entries')

    # Populate vector database
    for i, chunk in enumerate(dataset):
        add_chunk_to_database(chunk)
        print(f'Added chunk {i+1}/{len(dataset)} to the database')

    # Chatbot
    input_query = input('Ask me a question: ')
    retrieved_knowledge = retrieve(input_query)

    print('Retrieved knowledge:')
    for chunk, similarity in retrieved_knowledge:
        print(f' - (similarity: {similarity:.2f}) {chunk}')

    instruction_prompt = f'''You are a helpful chatbot.
Use only the following pieces of context to answer the question. Don't make up any new information:
{'\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])}
'''

    # Call Groq API for LLM response
    print('Chatbot response:')
    response_text, prompt_tokens, completion_tokens = call_llm(
        system=instruction_prompt,
        user=input_query,
        label="RAG Chat"
    )
    print(response_text)
    print(
        f'\n[Tokens - Prompt: {prompt_tokens}, Completion: {completion_tokens}]')


if __name__ == '__main__':
    main()
