import pandas as pd
import os
import tiktoken
import itertools
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from config.config import OPENAI_API_KEY, PINECONE_API_KEY

INDEX_NAME = "product-matching"
VECTOR_DIMENSION = 1536  # Zgodne z modelem OpenAI

# połączenie z open ai
client = OpenAI(api_key=OPENAI_API_KEY)

# połączenie z Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(INDEX_NAME)

# Pobranie rekordów o identyfikatorach 'id-1' i 'id-2' z przestrzeni nazw 'example-namespace'
response = index.fetch(ids=['6309', 'id-2'], namespace='example-namespace')

if __name__ == "__main__":
    print('sprawdzanie')