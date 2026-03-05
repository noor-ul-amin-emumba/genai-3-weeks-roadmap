import json

from sentence_transformers import SentenceTransformer
import importlib
import sys
from pathlib import Path
from pypdf import PdfReader


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


# ---------------------------------------------------------------------------
# RAG Functions
# ---------------------------------------------------------------------------

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


def exact_match_semantic(prediction: str, ground_truth: str) -> float:
    """
    Return 1.0 if prediction semantically matches ground truth; 0.0 otherwise.
    Uses embedding-based semantic similarity for answerable questions.
    For unanswerable questions, checks for refusal indicators.
    """
    if ground_truth.strip().upper() == "NOT IN DOCUMENTS":
        # Check for refusal / uncertainty
        refusal_keywords = [
            "not in", "not mentioned", "not provided", "not found",
            "not available", "not contain", "cannot find", "cannot answer",
            "i don't know", "i do not know", "no information",
            "unable to find", "not discussed", "not stated", "not specified",
            "isn't mentioned", "is not mentioned", "not present",
        ]
        pred_lower = prediction.lower()
        return 1.0 if any(kw in pred_lower for kw in refusal_keywords) else 0.0
    else:
        # Use semantic similarity for answerable questions
        try:
            gt_embedding = embedding_model.encode(ground_truth)
            pred_embedding = embedding_model.encode(prediction)
            similarity = cosine_similarity(gt_embedding, pred_embedding)
            # Threshold: 0.7 means 70% semantic similarity
            return 1.0 if similarity >= 0.7 else 0.0
        except Exception as e:
            print(f"Warning: semantic similarity calculation failed: {e}")
            return 0.0


# ---------------------------------------------------------------------------
# PDF Text Extraction
# ---------------------------------------------------------------------------

def extract_pdf_text(pdf_path: Path, max_chars: int = 30_000) -> str:
    """Extract plain text from a PDF file using pypdf."""

    reader = PdfReader(str(pdf_path))
    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text.strip())
    return pages_text


def main():
    # Load the dataset
    dataset_path = Path(__file__).parent / 'ai_foundations.pdf'
    questions_path = Path(__file__).parent / 'question_set.json'

    dataset = extract_pdf_text(dataset_path)
    print(f'Loaded {len(dataset)} entries from PDF')

    # Populate vector database
    for i, chunk in enumerate(dataset):
        add_chunk_to_database(chunk)
        print(f'Added chunk {i+1}/{len(dataset)} to the database')

    # Chatbot
    # input_query = input('Ask me a question: ')

    question_set = []
    with open(questions_path, encoding='utf-8') as file:
        question_set = json.load(file)
        print(f'Loaded {len(question_set)} questions')

    for question in question_set:
        retrieved_knowledge = retrieve(question["question"])

        print('\n' + '='*80)
        print(f"Question ID: {question['id']}")
        print(f"Category: {question['category']}")
        print(f"\nExact Question: {question['question']}")
        print('='*80)

        instruction_prompt = f'''You are a helpful and precise assistant. Answer the question based ONLY.
        on the provided document context. If the answer is not in the context, 
        say 'The answer is not found in the provided documents.' 
        Be concise and accurate.
        {'\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])}
        '''

        # Call Groq API for LLM response
        print(f'\nCalling LLM...')
        response_text, prompt_tokens, completion_tokens = call_llm(
            system=instruction_prompt,
            user=question["question"],
            label="RAG Chat"
        )

        # Evaluate response
        score = exact_match_semantic(response_text, question["ground_truth"])
        result = "PASS" if score == 1.0 else "FAIL"

        print(f'\nLLM Response:\n{response_text}')
        print(f'\nGround Truth:\n{question["ground_truth"]}')
        print(
            f'\n[Result: {result}] [Tokens - Prompt: {prompt_tokens}, Completion: {completion_tokens}]')


if __name__ == '__main__':
    main()
