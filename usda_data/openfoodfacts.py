import requests


def get_nutritional_info(product_name, country="Poland"):
    # Funkcja do wykonania zapytania do API
    def fetch_data(query):
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": query,  # Wyszukiwana fraza
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "tagtype_0": "countries",
            "tag_contains_0": "contains",
            "tag_0": country,
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            # Zwraca produkty, jeśli są
            if data["count"] > 0:
                return data["products"]
        return []

    # Wyszukiwanie dla pełnej frazy
    products = fetch_data(product_name)

    # Jeśli nie znaleziono wyników, spróbuj kombinacje słów
    if not products:
        words = product_name.split()  # Rozdzielamy frazę na słowa
        for i in range(len(words), 0, -1):  # Próba kombinacji 1 do n słów
            for j in range(len(words) - i + 1):
                query = ' '.join(words[j:j + i])
                products = fetch_data(query)
                if products:  # Jeśli znalazło produkty, przerwij
                    break
            if products:
                break

    # Jeśli produkty zostały znalezione, wyciągnij informacje o składnikach odżywczych
    if products:
        nutritional_info = []
        for product in products:
            nutriments = product.get('nutriments', {})
            nutrients = {
                'product_name': product.get('product_name', 'N/A'),
                'energy_kcal': nutriments.get('energy-kcal', 'N/A'),
                'energy_kj': nutriments.get('energy-kj', 'N/A'),
                'fat': nutriments.get('fat', 'N/A'),
                'saturated_fat': nutriments.get('saturated-fat', 'N/A'),
                'carbohydrates': nutriments.get('carbohydrates', 'N/A'),
                'sugars': nutriments.get('sugars', 'N/A'),
                'fiber': nutriments.get('fiber', 'N/A'),
                'proteins': nutriments.get('proteins', 'N/A'),
                'salt': nutriments.get('salt', 'N/A'),
                'sodium': nutriments.get('sodium', 'N/A')
            }
            nutritional_info.append(nutrients)

        return nutritional_info
    return []


# Przykład użycia funkcji
product_name = "marinero"
nutritional_info = get_nutritional_info(product_name)

# Wyświetlanie wyników
if nutritional_info:
    for info in nutritional_info:
        print(info)
else:
    print("Brak wyników.")
