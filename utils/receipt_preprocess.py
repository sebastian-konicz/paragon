import os
import pandas as pd
import json
import re
from datetime import datetime

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)

def preprocess_receipts(files):
    all_data = []

    for file in files:
        # Extract ID from file name
        if isinstance(file, str):
            file_name = file
            data = json.loads(file)
        else:
            file_name = file.name
            data = json.load(file)

        # wyciągniecie timestamp i zmiana w date object
        date_string = data['header'][2]['headerData']['date']
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

        # wyciągamy datę w formacie RRRR-MM-DD
        date_value = date_object.strftime("%Y-%m-%d")

        # wyciągamy czas w formacie HH:MM:SS
        time_value = date_object.strftime("%H:%M:%S")

        items = data['body']
        rows = []
        current_sell_line = None

        for item in items:
            if 'sellLine' in item:
                current_sell_line = item['sellLine']
                row = {
                    'date': date_value,
                    'time': time_value,
                    'product_name_raw': current_sell_line['name'],
                    'vatId': current_sell_line['vatId'],
                    'price': current_sell_line['price'],
                    'total': current_sell_line['total'],
                    'quantity': current_sell_line['quantity'],
                    'discount_base': None,
                    'discount_value': None,
                    'isDiscount': None,
                    'isPercent': None
                }
                rows.append(row)
            elif 'discountLine' in item and len(rows) > 0:
                discount_line = item['discountLine']
                rows[-1]['discount_base'] = discount_line['base']
                rows[-1]['discount_value'] = discount_line['value']
                rows[-1]['isDiscount'] = discount_line['isDiscount']
                rows[-1]['isPercent'] = discount_line['isPercent']

        df = pd.DataFrame(rows)
        df['product_name'] = df['product_name_raw'].apply(lambda x: str(x).rstrip(" ABC"))
        df['product_name'] = df['product_name'].apply(lambda x: re.sub(
            r'(?<![A-ZĄĆĘŁŃÓŚŹŻ])(?=[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż])|(?<=[a-ząćęłńóśźż])(?=[A-ZĄĆĘŁŃÓŚŹŻ])|(?<=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż])(?=\d)',
            ' ', x))
        df['product_name'] = df['product_name'].apply(
            lambda x: re.sub(r'(?<=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9])\.(?=[a-zA-ZĄĆĘŁŃÓŚŹŻąćęłńóśźż0-9])', ' ', x))
        df['product_name'] = df['product_name'].apply(lambda x: re.sub(r'\s+', ' ', x).strip())

        def extract_measurements(s):
            match = re.search(r'(\d+(?:,\d+)?)(ml|l|kg|g|ML|L|KG|G|szt)', s)
            if match:
                measure_value = match.group(1)
                measure = match.group(2).lower()
                return pd.Series([measure_value, measure])
            return pd.Series([None, None])

        df[['measure_value', 'measure']] = df['product_name'].apply(extract_measurements)
        df['measure_value'] = df['measure_value'].apply(lambda x: float(str(x).replace(',', '.')) if str(x) != 'None' else x)
        df['total_final'] = df.apply(
            lambda x: x['discount_base'] - x['discount_value'] if x['isDiscount'] == True else x['total'], axis=1)
        df['total_pln'] = df['total_final'].apply(lambda x: x / 100)
        df.fillna('', inplace=True)
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.to_excel(f'paragon_data_combined.xlsx', index=False)
    return combined_df

if __name__ == "__main__":
    files = ['paragon_2411135756125160.json', 'paragon_2.json']
    preprocess_receipts(files)