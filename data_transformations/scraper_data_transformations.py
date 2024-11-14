import os
import re
import time
import pandas as pd

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy

def data_transformation():

    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())

    # Wczytanie pliku JSON
    df = pd.read_excel(cwd + f'/data/biedronka_nutrition_all_product_types.xlsx')

    # upewnianie się że id ma dobry format
    df['item_id'] = df['item_id'].apply(lambda x: str(x).zfill(10))

    # Zmiana nazw wybranych kolumn
    df.rename(columns={'wartość': 'nutri_mesurement',
                       'item_name': 'item_name_raw',
                       'monounsaturated fatty acids': 'mono_unsat_fatty_acids',
                       'polyunsaturated fatty acids': 'poly_unsat_fatty_acids'}, inplace=True)

    # kategorie dla których nie ma informacji odżywczych
    non_nutrient_cat = ['drogeria', 'dla-zwierzat', 'dla-domu']
    df['nutri_category_flag'] = df['item_type'].apply(lambda x: 'N' if x in non_nutrient_cat else 'Y')

    # funkcja do wyodrębniania pojemności, jednostki miray i suchej nazwy produktu
    def extract_measurements(s):
        match = re.search(r'(\d+(?:,\d+)?)\s?(ml|l|kg|g|ML|L|KG|G|szt|SZT)', s)
        if match:
            measure_value = match.group(1)
            measure = match.group(2).lower()  # Konwertuj jednostki miar na małe litery
            # Usuń znalezioną miarę i jednostkę z nazwy
            modified_name = re.sub(r'\b' + re.escape(match.group(0)) + r'\b', '', s).strip().lower()
            return pd.Series([measure_value, measure, modified_name])
        return pd.Series([None, None, s])

    # Zastosowanie funkcji do kolumny 'string'
    df[['measure_value', 'measure', 'item_name_amd']] = df['item_name_raw'].apply(extract_measurements)

    # 'w portcji na 100 g' na 100 i g
    def extract_nutri_measure(s):
        match = re.search(r'(\d+(?:,\d+)?)\s?(ml|l|kg|g|ML|L|KG|G|szt|SZT)', str(s))
        if match:
            measure_value = match.group(1)
            measure = match.group(2).lower()  # Konwertuj jednostki miar na małe litery
            return pd.Series([measure_value, measure])
        return pd.Series([None, None])

    # Zastosowanie funkcji do kolumny 'string'
    df[['nutri_measure_value', 'nutri_measure']] = df['nutri_mesurement'].apply(extract_nutri_measure)

    # usuwanie kcal i branie samej wartości:
    df['kcal'] = df['kcal'].str.replace(' kcal', '').str.strip()
    df['kcal'] = df['kcal'].str.replace(',', '.').astype(float)

    nutri_list = ['fat', 'saturated_fat', 'carbohydrates', 'sugar', 'fiber', 'protein', 'salt',
                  'mono_unsat_fatty_acids', 'poly_unsat_fatty_acids', 'polyols', 'starch', 'omega3']

    # wycinanie gramów z wartości odżywczych i zmiana na float
    for nutrient in nutri_list:
        df[nutrient] = df[nutrient].str.replace(' g', '').str.strip()
        df[nutrient] = df[nutrient].str.replace(',', '.').astype(float)

    # ujednolicanie tekstu
    def preprocess_text(text):
        # Zmiana na lowercase
        text = text.lower()

        # Zamiana polskich znaków na ich odpowiedniki
        polish_char_map = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
        }
        for polish_char, replacement in polish_char_map.items():
            text = text.replace(polish_char, replacement)

        # Usunięcie znaków specjalnych
        text = re.sub(r'[^\w\s]', '', text)

        return text

    df['item_name_amd'] = df['item_name_amd'].apply(preprocess_text)

    df = df[['item_id', 'item_name_raw', 'item_name_amd', 'item_type',
             'measure_value', 'measure',
             'nutri_category_flag', 'nutrition_flag',
             'nutri_measure_value', 'nutri_measure',
             'kcal', 'kJ',
             'fat', 'saturated_fat',
             'carbohydrates', 'sugar', 'fiber',
             'protein', 'salt',
             'mono_unsat_fatty_acids', 'poly_unsat_fatty_acids',
             'polyols', 'starch', 'omega3'
              ]]

    df.sort_values(by=['item_type', 'item_name_amd'], ascending=[True, True], inplace=True)

    print(df.head(20))
    df.to_excel(cwd + f'/data/final/biedronka_nutrition_all_amd.xlsx', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

    return df

if __name__ == "__main__":
    data_transformation()
