from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [
    "This is the first document.",  
    "This document is the second document.",

]

vector = embedding.embed_documents(texts)
print(vector)





