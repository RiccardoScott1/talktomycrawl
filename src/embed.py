import os
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document


def embed_documents(result, supabase_client):
    """
    This function loads documents from a text file, splits them into chunks, and stores them in a Supabase vector store.
    """

    # split documents
    doc =  Document(
        id=result['url'],
        page_content=result['markdown'], 
        metadata={
            'metadata':result['metadata'],
            'url':result['url'],
        }
        )
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    docs = text_splitter.split_documents([doc])

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = SupabaseVectorStore.from_documents(
        docs,
        embeddings,
        client=supabase_client,
        table_name="documents",
        query_name="match_documents",
        chunk_size=500,
    )