SYSTEM_PROMPT = """
You are a helpful and verified assistant. Always provide accurate information based on the provided context.
If you don't know the answer, say so.
"""

RAG_PROMPT = """
Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Verified Answer:
"""