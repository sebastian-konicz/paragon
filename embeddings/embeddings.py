import pandas as pd
import os
import tiktoken
import itertools
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from config.config import OPENAI_API_KEY, PINECONE_API_KEY

INDEX_NAME = "product-matching_amd"
VECTOR_DIMENSION = 1536  # Zgodne z modelem OpenAI

# połączenie z open ai
client = OpenAI(api_key=OPENAI_API_KEY)

# połączenie z Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
existing_indexes = [index["name"] for index in pc.list_indexes()]

if INDEX_NAME in existing_indexes:
    # user_input = input(f"Indeks '{INDEX_NAME}' już istnieje. Czy chcesz go nadpisać? (y/n): ").strip().lower()
    user_input = 'y'
    if user_input == "y":
        pc.delete_index(INDEX_NAME)  # Usunięcie starego indeksu
        print(f"✅ Indeks '{INDEX_NAME}' został usunięty.")

        # Tworzenie nowego indeksu
        print(f"🔄 Tworzę nowy indeks '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=VECTOR_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        print(f"✅ Indeks '{INDEX_NAME}' został utworzony.")
    else:
        print(f"❌ Indeks '{INDEX_NAME}' pozostaje bez zmian.")
else:
    # Tworzenie nowego indeksu tylko, jeśli wcześniej nie istniał
    print(f"🔄 Indeks '{INDEX_NAME}' nie istnieje. Tworzę nowy...")
    pc.create_index(
        name=INDEX_NAME,
        dimension=VECTOR_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    print(f"✅ Indeks '{INDEX_NAME}' został utworzony.")

index = pc.Index(INDEX_NAME)

def generate_embedding(text):
    """Tworzy embedding dla danego tekstu."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def store_embeddings(text, id):
    """Generuje embeddingi dla produktów sklepowych."""
    print(id)
    embedding = generate_embedding(text)
    vector = (str(id), embedding)

    return vector

def upsert_to_pinecone(batch):
   index.upsert(batch)

# Funkcja do dzielenia listy na mniejsze partie
def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def embedding_cost(df):
    """Oblicza koszt generowania embeddingów dla produktów sklepowych."""
    documents = df["item_name_amd"].tolist()
    enc = tiktoken.encoding_for_model("text-embedding-3-small")
    total_tokens = sum(len(enc.encode(text)) for text in documents)
    cost_per_1M_tokens = 0.02
    cost = total_tokens * cost_per_1M_tokens / 1000000
    print('cost:', cost)
    print('total tokens:', total_tokens)
    return cost

# Funkcja do dzielenia listy na mniejsze partie
def chunk_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

if __name__ == "__main__":
    cwd = str(os.getcwd())
    df = pd.read_excel(cwd + f"/data/raw/biedronka_nutrition_all_amd.xlsx")
    print(df.head(5))
    batch_size = 100
    # store_embeddings(df)
    ids = df['item_id'].to_list()
    text = df['item_name_amd'].to_list()
    embedding_cost(df)
    vectors = [store_embeddings(text, id) for text, id in zip(text, ids)]
    for batch in chunk_list(vectors, batch_size):
        # Przesyłanie partii do Pinecone
        # (zakładając, że masz funkcję upsert_to_pinecone)
        upsert_to_pinecone(batch)