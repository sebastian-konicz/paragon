import requests

def check_product_in_open_food_facts(product_name):
    url = f"https://world.openfoodfacts.org/api/v0/product/{product_name}.json"
    response = requests.get(url)
    if response.status_code == 200:
        product_data = response.json()
        if product_data.get("status") == 1:
            return product_data['product']
    return None