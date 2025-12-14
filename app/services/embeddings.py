from langchain_openai import OpenAIEmbeddings
from app.core.config import settings

embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)