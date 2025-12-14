from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.prompts import RAG_PROMPT
from app.models.chat import ChatResponse
from app.services.vector_store import load_vector_store
import os

def process_uploaded_file(file_path: str):
    documents = load_document(file_path)
    chunks = chunk_text(documents)
    create_vector_store(chunks)

def rag_pipeline(question: str) -> ChatResponse:
    vectorstore = load_vector_store()
    if not vectorstore:
        return ChatResponse(response="No documents uploaded yet.", sources=[])
    
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(openai_api_key=settings.openai_api_key, model="gpt-3.5-turbo")
    prompt = PromptTemplate.from_template(RAG_PROMPT)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    response = chain.invoke(question)
    # sources not implemented yet
    return ChatResponse(response=response, sources=[])