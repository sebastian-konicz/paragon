from pinecone import Pinecone, ServerlessSpec
from config.config import PINECONE_API_KEY

pc = Pinecone(api_key=PINECONE_API_KEY, pool_threads=30)

pc.create_index(
    name='datacamp-index',
    dimension=1536,
    spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    )
)

# pc.delete_index('datacamp-index')

index = pc.Index('datacamp-index')


print(index)
print(index.describe_index_stats())
print(pc.list_indexes())

vector_dims = [len(vector['values']) == 1536 for vector in vectors]
all(vector_dims)