import os
import time
import pandas as pd
import tiktoken
from rapidfuzz import process
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
    print(product_list[0])
    product = product_list[0]

    # baza danych
    product_database = pd.read_excel(parent_directory + f'/data/biedronka_nutrition_all_product_types.xlsx')

    print(product_database.head(5))
    product_db_name_list = product_database['item_name'].to_list()

    # open ai settings
    client = OpenAI(api_key=OPENAI_API_KEY)
    model="gpt-4o"

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def find_best_match(model, product, product_db_name_list):
        # prepocessing with rapid fuzz
        print('fuzz')
        top_matches = process.extract(product, product_db_name_list, limit=10)
        print(top_matches)

        # -------------prompt
        prompt = f"""
        Dopasuj nazwe produktu w potrójnych cydzysłowiu  '''{product}''' z pełną nazwą w bazie danych: {top_matches}
        """
        encoding = tiktoken.encoding_for_model(model)
        prompt_tokens = len(encoding.encode(prompt))

        print("PROMPT:", prompt)
        print("PROMPT TOKENS:", prompt_tokens)

        try:
            # Generacja odpowiedzi przy użyciu modelu
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )

            # Pobranie dopasowanej nazwy produktu
            chat_response = response.choices[0]
            return chat_response
        except AuthenticationError as e:
            print(f"OpenAI API failed to authenticate: {e}")
            pass
        except RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass
        except Exception as e:
            print(f"Unable to generate a response. Exception: {e}")
            pass

    response = find_best_match(model, product, product_db_name_list)

    print("RESPONSE:\n", response)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    open_ai()

