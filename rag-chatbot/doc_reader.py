import os
from llama_index.readers.file import DocxReader
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage
from pathlib import Path
from dotenv import load_dotenv
from definitions import ROOT_DIR

load_dotenv()  # Load the API key from the .env file to connect to a remote agent


def get_index(data, index_name):
    """
    This function fetches vector embeddings for a given folder and creates those embeddings if the folder does not exist
    """
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index


# Create an engine that reads the UK Word document in the data directory specifically. Part of uk_data tool
doc_path = Path(os.path.join(ROOT_DIR, "rag-chatbot", "data", "UK.docx"))
uk_doc = DocxReader().load_data(file=doc_path)
uk_index = get_index(uk_doc, "uk_embeddings")
uk_engine = uk_index.as_query_engine()

# Create an engine that can read any document in the varied_data directory. Part of varied_data tool
varied_data_path = os.path.join(ROOT_DIR, "rag-chatbot", "varied_data")
varied_docs = SimpleDirectoryReader(varied_data_path).load_data()
varied_index = get_index(varied_docs, "varied_embeddings")
varied_engine = varied_index.as_query_engine()
