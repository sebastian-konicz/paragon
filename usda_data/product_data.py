import requests
import json
import pandas as pd
from config.config import USDA_API_KEY

# Twój klucz API z FoodData Central
BASE_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy

def search_food(query, page_size=5, save_response=False):
    """
    https://fdc.nal.usda.gov/api-guide.html
    https://openfoodfacts.github.io/openfoodfacts-server/api/ref-v2/
    Funkcja wyszukuje produkty spożywcze na podstawie zapytania i zwraca podstawowe informacje.

    :param query: Nazwa produktu do wyszukania (np. "apple").
    :param page_size: Liczba wyników do wyświetlenia.
    :return: Lista wyników z informacjami o produktach.
    """
    params = {
        'api_key': USDA_API_KEY,
        'query': query,
        'pageSize': page_size,
        'dataType': ['Foundation', 'Survey (FNDDS)'],
        'requireAllWords': True
    }

    response = requests.get(BASE_URL, params=params)

    print(response)

    if response.status_code == 200:
        data = response.json()

        # Zapisz surową odpowiedź do pliku JSON, jeśli save_response jest True
        if data:
            with open('raw_response.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Surowa odpowiedź zapisana do pliku 'raw_response.json'")

        # Wybierz produkt z najwyższym 'score'
        foods = data.get('foods', [])
        if not foods:
            print("Brak wyników dla zapytania.")
            return None

        top_food = max(foods, key=lambda x: x.get('score', 0))
        return top_food
    else:
        print(f"Błąd: {response.status_code}")
        return None


def create_food_dataframe(food):
    """
    Funkcja tworzy DataFrame z informacji o produkcie spożywczym.

    :param food: Produkt spożywczy o najwyższym score.
    :return: DataFrame z informacjami o produkcie.
    """
    # Pobierz podstawowe informacje
    fdc_id = food.get('fdcId')
    description = food.get('description')
    food_category = food.get('foodCategory')

    # Przygotuj dane składników odżywczych
    nutrients_data = {nutrient['nutrientName']: f"{nutrient['value']} {nutrient['unitName']}"
                      for nutrient in food.get('foodNutrients', [])}

    # Połącz wszystkie dane w jeden słownik
    data = {
        'fdcId': fdc_id,
        'description': description,
        'foodCategory': food_category,
        **nutrients_data
    }

    # Utwórz DataFrame z jednego wiersza
    df = pd.DataFrame([data])
    return df


if __name__ == "__main__":
    query = 'onion'
    top_food = search_food(query, save_response=True)

    if top_food:
        df = create_food_dataframe(top_food)
        print(df)
    else:
        print("Nie znaleziono produktów.")