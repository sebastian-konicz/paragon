import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy

column_dict = {'fat': ('tłuszcz', 'zawartość tłuszczów (ogólnie)'),
               'saturated_fat': (
               'w tym kwasy tłuszczowe nasycone', 'kwasy tłuszczowe nasycone', 'w tym kasy tłuszczowe nasycone',
               'tym nasycone', 'w tym kwasy tłuszczowe', 'tym kwasy tłuszczowe nasycone',
               'w tym nasycone kwasy tłuszczowe', 'w tym kwasy tłuszczowe nasycone '),
               'monounsaturated fatty acids': ('kwasy tłuszczowe jednonienasycone', 'w tym kwasy tłuszczowe jednonienasycone'),
               'polyunsaturated fatty acids': ('kwasy tłuszczowe wielonienasycone', 'w tym kwasy tłuszczowe wielonienasycone'),
               'carbohydrates': ('węglowodany', 'zawartość węglowodanów'),
               'sugar': ('w tym cukry', 'cukry', 'w tym cukry ', 'w tym cukier'),
               'fiber': ('błonnik', 'zawartość błonnika'),
               'protein': ('białko', 'zawartość białek'),
               'salt': ('sól', 'zawartość soli'),
               'kcal': ('wartość energetyczna kcal', 'wartość energetyczna  kcal', 'wartość energetyczna kcal kcal',
                        'wartość odżywcza (w 100 g produktu) kcal'),
               'kJ': ('wartość energetyczna kJ', 'wartość energetyczna  kJ', 'wartość odżywcza (w 100 g produktu) kJ'),
               'starch': ('skrobia', 'zawartość skrobii', 'w tym skrobia'),
               'polyols': ('alkohole wielowodorotlenowe - poliole', 'w tym poliole'),
               'omega3': ('omega 3', 'omega_3'),
               'ergokalcyferol': ('ergokalcyferol lub witamina d2', 'witamina d2'),
               'dha': ('w tym dha (kwas dokozaheksaenowy)', 'w tym dha')
               }

def rename_columns(df, column_dict):
    # Tworzymy mapowanie nazw kolumn
    column_map = {}
    for key, value_tuple in column_dict.items():
        for value in value_tuple:
            column_map[value] = key

    # Zmieniamy nazwy kolumn w DataFrame
    new_columns = [column_map.get(col, col) for col in df.columns]
    df.columns = new_columns
    return df

def nutrition_scraper(product_type, i):

    cwd = os.getcwd()

    file_path = f'biedronka_items_{product_type}_{i}'

    # Ścieżka do folderu
    folder_path = cwd + f'/data/interim/{product_type}'

    # Sprawdzenie, czy folder istnieje
    if not os.path.exists(folder_path):
        # Tworzenie folderu, jeśli nie istnieje
        os.mkdir(folder_path)
        print(f'Folder "{folder_path}" został utworzony.')
    else:
        print(f'Folder "{folder_path}" już istnieje.')

    # Ustaw nagłówki, aby symulować przeglądarkę
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }

    # ładowanie pliku
    df = pd.read_csv(cwd + f'/data/raw/{product_type}/{file_path}.csv')

    df['item_id'] = df['item_id'].apply(lambda x: str(x).zfill(10))

    items_id = df['item_id'].to_list()
    items_name = df['item_name'].to_list()
    items_type = df['item_type'].to_list()
    items_links = df['item_link'].to_list()

    items_dict = dict(zip(items_id, items_links))

    result_dict = {k: (v1, v2, v3) for k, v1, v2, v3 in zip(items_id, items_name, items_type, items_links)}

    df_list = []
    for id, value in result_dict.items():

        item_name = value[0]
        item_type = value[1]
        url = value[2]
        print(id, item_name, item_type, url)

        # Wykonaj zapytanie HTTP GET
        response = requests.get(url, headers=headers)

        # Przetwórz HTML przy pomocy BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        if response.status_code == 200:
            # puste listy do wypełnienia
            header_list = []
            value_list = []

            header_list.append('item_id')
            value_list.append(id)

            header_list.append('item_name')
            value_list.append(item_name)

            header_list.append('item_type')
            value_list.append(item_type)

            # Znajdź tabele z wartościami odżywczymi'
            table = soup.find("table", class_="product-description__table")
            if table:
                header_list.append('nutrition_flag')
                value_list.append('Y')

                thead = table.find('thead')
                if thead:
                    ths = thead.find_all('th')
                    th_header = ths[0].text.lower()
                    th_value = ths[1].text.lower()
                    header_list.append(th_header)
                    value_list.append(th_value)
                else:
                    header_list.append('wartość')
                    value_list.append('w porcji 100 g')

                rows = table.find_all('tr')

                for row in rows[:-1]:
                    cols = row.find_all('td')
                    # print(f'column_name: {cols[0].text}', f'| column_value: {cols[1].text}')
                    header = cols[0].text.lower()
                    if cols[1].text[-4:] == 'kcal':
                        header = header + ' kcal'
                        value = cols[1].text.lower()
                    elif cols[1].text[-2:] == 'kJ':
                        header = header + ' kJ'
                        value = cols[1].text.lower()
                    else:
                        value = cols[1].text.lower()
                    header_list.append(header)
                    value_list.append(value)
                # print(header_list)
                # print(value_list)
            else:
                header_list.append('nutrition_flag')
                value_list.append('N')
            df = pd.DataFrame([value_list], columns=header_list)

            df_renamed = rename_columns(df, column_dict)

            print(df_renamed)
            df_list.append(df_renamed)
        else:
            print("Błąd pobierania strony:", response.status_code)

    data = pd.concat(df_list)
    print(data)

    data.to_csv(cwd + f'/data/interim/{product_type}/biedronka_items_nutrition_{product_type}_{i}.csv', index=False)

    return data
if __name__ == "__main__":
    product_type = 'piekarnia'
    i ='test'
    nutrition_scraper(product_type, i)