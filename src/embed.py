from langchain_community.vectorstores import SupabaseVectorStore
from langchain_text_splitters import HTMLSemanticPreservingSplitter  # Preserves HTML structure while splitting
from langchain_ollama import OllamaEmbeddings  # Interface for embedding with Ollama models
from langchain.docstore.document import Document  # Document object used by LangChain
from supabase import Client

def embed_documents(result:dict, supabase_client:Client):
    """
    Splits a crawled HTML document into semantic chunks, generates embeddings using an Ollama model,
    and stores the resulting vectors in a Supabase vector store.
    """

    # Define which HTML headers to split on (semantic chunking)
    headers_to_split_on = [
        ('h1', 'header1'),
        ('h2', 'header2'),
        ('h3', 'header3'),
    ]

    # Create the text splitter with a max chunk size
    text_splitter = HTMLSemanticPreservingSplitter(
        headers_to_split_on=headers_to_split_on,
        max_chunk_size=1000
    )

    # Split the cleaned HTML into smaller semantically meaningful chunks
    docs = text_splitter.split_text(result['cleaned_html'])

    # Add metadata and unique IDs to each chunked document
    for i, doc in enumerate(docs):
        doc.metadata = {
            'metadata': result['metadata'],
            'url': result['url'],
        }
        doc.id = result['url'] + '__' + str(i)  # Unique ID for each chunk

    # Initialize the Ollama embeddings model (using nomic-embed-text)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Store the embedded documents into Supabase vector store for later retrieval
    vector_store = SupabaseVectorStore.from_documents(
        docs,                         # List of chunked documents
        embeddings,                   # Embedding model
        client=supabase_client,       # Supabase client connection
        table_name="documents",       # Target table for vector storage
        query_name="match_documents", # Name of the query function for retrieval
        chunk_size=500,               # Batch size for upload
    )
