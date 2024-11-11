import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tiktoken
from sklearn.manifold import TSNE
from scipy.spatial import distance
from config.config import OPENAI_API_KEY
from openai import OpenAI, AuthenticationError, RateLimitError
from tenacity import (retry, stop_after_attempt, wait_random_exponential)

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy


def open_ai():
    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())
    parent_directory = os.path.dirname(cwd)

    # dane z paragonów
    df = pd.read_excel(parent_directory + f'/data/paragon_data_copy.xlsx')

    product_list = df['product_name'].to_list()
    product_dict_list = [{"paragon_item_name": name} for name in product_list]

    # baza danych
    product_database = pd.read_excel(parent_directory + f'/data/biedronka_nutrition_all_product_types.xlsx')
    product_database_list = product_database['item_name'].to_list()

    # open ai settings
    client = OpenAI(api_key=OPENAI_API_KEY)
    model="text-embedding-3-small"

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def embeddings(product_list):

        print("EMBEDDINGS INPUT:", product_list)

        try:
            # Generacja odpowiedzi przy użyciu modelu
            response = client.embeddings.create(
                model=model,
                input=product_list
            )

            # Pobranie dopasowanej nazwy produktu
            response_dict = response.model_dump()
            return response_dict
        except AuthenticationError as e:
            print(f"OpenAI API failed to authenticate: {e}")
            pass
        except RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass
        except Exception as e:
            print(f"Unable to generate a response. Exception: {e}")
            pass

    def create_embeddings(text):
        print("CREATE EMBEDDINGS INPUT:", text)

        try:
            # Generacja odpowiedzi przy użyciu modelu
            response = client.embeddings.create(
                model=model,
                input=text
            )

            # Pobranie dopasowanej nazwy produktu
            response_dict = response.model_dump()
            return [data['embedding'] for data in response_dict['data']]
        except AuthenticationError as e:
            print(f"OpenAI API failed to authenticate: {e}")
            pass
        except RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass
        except Exception as e:
            print(f"Unable to generate a response. Exception: {e}")
            pass

    def find_n_closest(query_vector, embeddings, n=3):
        distances = []

        for index, embedding in enumerate(embeddings):
            dist = distance.cosine(query_vector, embedding)
            distances.append({"distance": dist, "index": index})
        distances_sorted = sorted(distances, key=lambda x: x["distance"])
        return distances_sorted[0:n]


    # response_dict = embeddings(product_list)
    #
    # for i, product in enumerate(product_dict_list):
    #     product['embedding'] = response_dict['data'][i]['embedding']

    text = 'Krasnystaw Kefir 420 g'
    search_embedding = create_embeddings(text)[0]
    product_embeddings = create_embeddings(product_list)

    hits = find_n_closest(search_embedding, product_embeddings)
    for hit in hits:
        product = product_dict_list[hit['index']]
        print(product['paragon_item_name'])

    distances = []
    for product in product_dict_list:
        dist = distance.cosine(search_embedding, product['embedding'])
        distances.append(dist)

    min_dist_ind = np.argmin(distances) # zwraca indeks najlepszego dopasowania
    print(product_dict_list[min_dist_ind]['paragon_item_name'])

    # embeddings = [product['embedding'] for product in product_dict_list]
    #
    # tsne = TSNE(n_components=2, perplexity=5)
    # embeddings_2d = tsne.fit_transform(np.array(embeddings))
    #
    # plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
    #
    # product_names = [product['paragon_item_name'] for product in product_dict_list]
    # for i, product_name in enumerate(product_names):
    #     plt.annotate(product_name, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
    # plt.show()

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    open_ai()

