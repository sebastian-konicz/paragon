import os
import time
import pandas as pd
import tiktoken
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

    # dane
    df = pd.read_excel(parent_directory + f'/data/paragon_data_copy.xlsx')

    product_list = df['product_name'].to_list()

    print(product_list)

    client = OpenAI(api_key=OPENAI_API_KEY)
    model = "gpt-4o"

    system_prompt = f"""
    Jesteś pomocnym asystentem, który odpowiada dokładnie z instrukcjami. 
    Jeśli nie masz dokładnych informacji to ich nie zmyślasz tylko pozostawiasz puste"""

    prompt = f"""
    W potrójnym cudzysłowiu znajduje się lista produktów spożywczych. Wyciągnij dla nich dane o zawartości składników odżywczych
    '''{product_list}'''
    """

    encoding = tiktoken.encoding_for_model(model)
    system_prompt_tokens = len(encoding.encode(system_prompt))
    prompt_tokens = len(encoding.encode(prompt))

    print('----PROMPTS----')
    print("SYSTEM PROMPT:", system_prompt)
    print("PROMPT:", prompt)
    print('----TOKENS----')
    print("SYSTEM PROMPT TOKENS:", system_prompt_tokens)
    print("PROMPT TOKENS:", prompt_tokens)

    message = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    function_definition = [{
                            'type': 'function',
                            'function': {
                                'name': 'extract_nutrition',
                                'description': 'Wyciągnij informację o zawartości poszczególnych składników odżywczych na 100 gram dla danego produktu',
                                'parameters': {
                                    'type': 'object',
                                    'properties':{
                                        'item_name':        {'type': 'string', 'description': 'nazwa produktu'},
                                        'kcal':             {'type': 'string', 'description': 'liczba kalorii'},
                                        'fat':              {'type': 'string', 'description': 'liczba gramów tłuszczu'},
                                        'saturated_fat':    {'type': 'string', 'description': 'liczba gramów nasyconych kwasów tłuszczowych'},
                                        'carbohydrates':    {'type': 'string', 'description': 'liczba gramów węglowodanów'},
                                        'sugar':            {'type': 'string', 'description': 'liczba gramów cukru'},
                                        'fiber':            {'type': 'string', 'description': 'liczba gramów błonnika'},
                                        'protein':          {'type': 'string', 'description': 'liczba gramów białka'},
                                        'salt':             {'type': 'string', 'description': 'liczba gramów soli'}
                                    }
                                }
                            }
                            }]

    print(function_definition)

    # @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    # def get_response(model, message, function_definition):
    #     try:
    #         response = client.chat.completions.create(
    #             model="gpt-4o",
    #             messages=message,
    #             tools=function_definition,
    #             temperature=0.25
    #         )
    #     except AuthenticationError as e:
    #         print(f"OpenAI API failed to authenticate: {e}")
    #         pass
    #     except RateLimitError as e:
    #         print(f"OpenAI API request exceeded rate limit: {e}")
    #         pass
    #     except Exception as e:
    #         print(f"Unable to generate a response. Exception: {e}")
    #         pass
    #
    #     return response.choices[0]
    #
    # response = get_response(model, message, function_definition)
    #
    # print("RESPONSE:\n", response.message.content)
    # print("RESPONSE:\n", response.message.tool_calls[0].function.arguments)


    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    open_ai()

