import pandas as pd
from transformers import pipeline

data = pd.read_excel(f'paragon_data.xlsx')

product_list = data['product_name'].to_list()
print(product_list)

# Załaduj pipeline do rozpoznawania encji
model = pipeline("fill-mask", model="allegro/herbert-large-cased")

# Funkcja do wyciągania produktów z tekstu
def extract_products_from_text(product):
    products = model(product)
    return products

for product in product_list:
    extracted_products = extract_products_from_text(product)
    print(extracted_products)