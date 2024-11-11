import chromadb
import os
import sys
# from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from config.config import OPENAI_API_KEY

# client = chromadb.PersistentClient(path="/path/to/save/to")

print(os.path.dirname(sys.executable))

# collection = client.create_collection(
#     name="netflix_titles",
#     embedding_function=OpenAIEmbeddingFunction(
#         model_name="text-embedding-3-small",
#         api_key=OPENAI_API_KEY)
# )

# # List the collections
# print(client.list_collections())