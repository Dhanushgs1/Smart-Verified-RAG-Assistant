from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    for doc in documents:
        chunks.extend(text_splitter.split_documents([doc]))
    return chunks