import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import config

db_path = config.DB_PATH
collection_name = config.COLLECTION_NAME

chroma_client = chromadb.PersistentClient(path=db_path)
image_loader = ImageLoader()
multimodal_ef = OpenCLIPEmbeddingFunction()

multimodal_db = chroma_client.get_collection(
    name=collection_name,
    embedding_function=multimodal_ef,
    data_loader=image_loader
)
