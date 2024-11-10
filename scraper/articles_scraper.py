import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Ustawienia wyświetlania w Pandas, aby wyświetlać wszystkie kolumny
pd.set_option('display.max_columns', None)  # Brak limitu na liczbę kolumn
pd.set_option('display.width', None)  # Brak limitu szerokości wyświetlania
pd.set_option('display.max_rows', None)  # Opcjonalnie, wyświetlanie wszystkich wierszy

def articles_scraper(product_type):
    cwd = os.getcwd()

    title = product_type.upper()
    print(f'-------------------------------------------------------')
    print(f'--------------------{title}----------------------------')
    print(f'-------------------------------------------------------')

    # Ścieżka do folderu
    folder_path = cwd + f'/data/raw/{product_type}'

    # Sprawdzenie, czy folder istnieje
    if not os.path.exists(folder_path):
        # Tworzenie folderu, jeśli nie istnieje
        os.mkdir(folder_path)
        print(f'Folder "{folder_path}" został utworzony.')
    else:
        print(f'Folder "{folder_path}" już istnieje.')


    # variables
    pages_text = '/?page='

    # Ustaw URL strony do pobrania
    url = f"https://zakupy.biedronka.pl/{product_type}"


    # Ustaw nagłówki, aby symulować przeglądarkę
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }

    # Wykonaj zapytanie HTTP GET
    response = requests.get(url, headers=headers)

    # -------------------------------------------------------------------
    # wyciąganie liczby stron z danej kategori
    # -------------------------------------------------------------------
    if response.status_code == 200:
        # Przetwórz HTML przy pomocy BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Znajdź wszystkie elementy <div> o klasie 'nazwa-klasy'
        pagination = soup.find("div", class_="bucket-pagination")

        pages = pagination.find_all("a", class_="bucket-pagination__link")

        page_number_list = []
        for page in pages:
            number = int(page.text)
            page_number_list.append(number)
        max_page_value = max(page_number_list)
        print(f'page_number: {max_page_value}')
    else:
        print("Błąd pobierania strony:", response.status_code)

    # --------------------------------------------------------------------
    # wyciąganie nazw produktów i linków z poszczególnych stron
    # -------------------------------------------------------------------
    for page_number in range(1,max_page_value+1):
        full_url = url + pages_text + str(page_number)
        print('-------------------------------------')
        print(full_url)
        print('-------------------------------------')

        # Wykonaj zapytanie HTTP GET
        response = requests.get(full_url, headers=headers)

        # Przetwórz HTML przy pomocy BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        if response.status_code == 200:
            # Znajdź wszystkie elementy <div> o klasie 'nazwa-klasy'
            div_elements = soup.find_all("div", class_="product-tile")

            item_id_list = []
            item_name_list = []
            item_link_list = []
            item_image_list = []

            for div_element in div_elements:
                item_id = div_element.get("data-itemid")
                item_id_list.append(item_id)
                # print(item_id)

                item_name = div_element.find("div", class_="thumb-link").get("data-title")
                item_name_list.append(item_name)
                # print(item_name)

                item_link = div_element.find("div", class_="thumb-link").get("data-href")
                item_link_list.append(item_link)
                # print(item_link)

                item_image_link = div_element.find("picture", class_="tile-image__container").find("source").get("data-srcset")
                item_image_list.append(item_image_link)
                # print(item_image_link)

            data = {
                'item_id': item_id_list,
                'item_name': item_name_list,
                'item_link': item_link_list,
                'item_image': item_image_list
            }

            # Tworzymy słownik, gdzie klucze to nazwy kolumn, a wartości to odpowiednie listy
            data = {
                'item_id': item_id_list,
                'item_name': item_name_list,
                'item_link': item_link_list,
                'item_image': item_image_list
            }

            # Tworzymy DataFrame
            df = pd.DataFrame(data)

            df['item_type'] = product_type

            # Wyświetlamy DataFrame
            print(df)

            df.to_csv(f'{folder_path}/biedronka_items_{product_type}_{page_number}.csv', index=False)
        else:
            print("Błąd pobierania strony:", response.status_code)

if __name__ == "__main__":
    product_type = 'piekarnia'
    articles_scraper(product_type)