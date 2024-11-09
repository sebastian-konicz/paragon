import json
import pandas as pd
from utils.ner_model import extract_products_from_text
from utils.open_food_facts import check_product_in_open_food_facts


def process_receipt(data):

    item_list = data['product_name'].to_list()
    print(item_list)

    results = []
    for item in item_list:
        product_name = item
        extracted_products = extract_products_from_text(product_name)
        print(extracted_products)

        for product in extracted_products:
            product_info = check_product_in_open_food_facts(product['word'])
            if product_info:
                results.append(f"Produkt {product['word']} znaleziony w bazie Open Food Facts!")
                results.append(f"Informacje: {product_info}")
            else:
                results.append(f"Produkt {product['word']} nie znaleziony w bazie Open Food Facts.")

    return results

if __name__ == "__main__":
    data = pd.read_excel(f'paragon_data.xlsx')
    print(data)