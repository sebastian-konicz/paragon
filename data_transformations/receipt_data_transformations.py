import os
import time
import pandas as pd
import json
import re
from datetime import datetime
import glob

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy

def preprocess_receipt(file):

    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())

    # --------------------------------------------------------------------------------------------------------------------------------
    # loading multiple files
    files = glob.glob(cwd + '/data/raw/*.json')

    print(files)

    data_list = []
    for file_path in files:
        with open(file_path, 'r') as file:
            data = json.load(file)
            data_list.append(data)

    print('dataframes count:', len(data_list))

    df_list = []

    for data in data_list:
        # wyciągniecie timestamp i zmiana w date object
        date_string = data['header'][2]['headerData']['date']
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

        # wyciągamy datę w formacie RRRR-MM-DD
        date_value = date_object.strftime("%Y-%m-%d")

        # wyciągamy czas w formacie HH:MM:SS
        time_value = date_object.strftime("%H:%M:%S")

        print("Data:", date_value)
        print("Czas:", time_value)

        items = data['body']

        # Lista na wiersze DataFrame
        rows = []

        # Tymczasowy słownik na dane sellLine
        current_sell_line = None

        # Iterowanie po danych
        for item in items:
            if 'sellLine' in item:
                # Zapisujemy sellLine od razu jako nowy wiersz bez discountLine
                current_sell_line = item['sellLine']
                row = {
                    'date': date_value,
                    'time': time_value,
                    'product_name_raw': current_sell_line['name'],
                    'vatId': current_sell_line['vatId'],
                    'price': current_sell_line['price'],
                    'total': current_sell_line['total'],
                    'quantity': current_sell_line['quantity'],
                    'discount_base': None,  # Wypełnimy to, jeśli znajdziemy discountLine
                    'discount_value': None,
                    'isDiscount': None,
                    'isPercent': None
                }
                rows.append(row)
            elif 'discountLine' in item and len(rows) > 0:
                # Aktualizujemy ostatni dodany wiersz o discountLine
                discount_line = item['discountLine']
                rows[-1]['discount_base'] = discount_line['base']
                rows[-1]['discount_value'] = discount_line['value']
                rows[-1]['isDiscount'] = discount_line['isDiscount']
                rows[-1]['isPercent'] = discount_line['isPercent']

        # tworzymy DataFrame z zebranych danych i dodajemy do listy dataframów
        df = pd.DataFrame(rows)
        df_list.append(df)

    df = pd.concat(df_list)

    df['product_name'] = df['product_name_raw'].apply(lambda x: str(x).rstrip(" ABC"))
    df['product_name'] = df['product_name'].apply(lambda x: re.sub(
        r'(?<![A-ZĄĆĘŁŃÓŚŹŻ])(?=[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż])|(?<=[a-ząćęłńóśźż])(?=[A-ZĄĆĘŁŃÓŚŹŻ])|(?<=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż])(?=\d)',
        ' ', x))
    df['product_name'] = df['product_name'].apply(
        lambda x: re.sub(r'(?<=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9])\.(?=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9])', ' ', x))
    df['product_name'] = df['product_name'].apply(lambda x: re.sub(r'\s+', ' ', x).strip())

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
    df[['measure_value', 'measure', 'product_name']] = df['product_name'].apply(extract_measurements)

    df['measure_value'] = df['measure_value'].apply(
        lambda x: float(str(x).replace(',', '.')) if str(x) != 'None' else x)

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

    df['product_name'] = df['product_name'].apply(preprocess_text)

    df['measure_value'].fillna('', inplace=True)
    df['measure'].fillna('', inplace=True)

    df['product_name_amd'] = df.apply(lambda x: x['product_name'] + ' ' + str(x['measure_value'])+ ' ' + str(x['measure']), axis=1)

    df['total_final'] = df.apply(
        lambda x: x['discount_base'] - x['discount_value'] if x['isDiscount'] == True else x['total'], axis=1)
    df['total_pln'] = df['total_final'].apply(lambda x: x / 100)

    df.fillna('', inplace=True)

    # Wyświetlenie DataFrame
    print(df.head(20))
    df.to_excel(cwd + f'/data/final/paragon_data_full.xlsx', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

    return df

if __name__ == "__main__":
    file_name = 'paragon_2411070103095160.json'
    base_path = os.path.dirname(__file__)  # Ścieżka do folderu, w którym jest skrypt (utils)
    data_folder = os.path.join(base_path, '..', 'data')  # Folder data w katalogu wyżej
    receipt_path = os.path.join(data_folder, file_name)  # Ścieżka do konkretnego pliku paragonu
    preprocess_receipt(receipt_path)
