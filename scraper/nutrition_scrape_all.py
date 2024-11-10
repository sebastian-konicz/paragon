import os
import pandas as pd
from scraper.nutrition_scraper import nutrition_scraper

def scrape_all_products():
    cwd = os.getcwd()

    product_dict  = {'artykuly-spozywcze': 40,
                     'dania-gotowe': 5,
                     'dla-domu': 19,
                     'dla-dzieci': 9,
                     'dla-zwierzat': 8,
                     'drogeria': 40,
                     'mieso': 8,
                     'mrozone': 4,
                     'nabial': 13,
                     'napoje': 8,
                     'owoce': 3,
                     'piekarnia': 4,
                     'warzywa': 5
                     }

    df_prodcut_list = []
    for product_type, files_number in product_dict.items():

        df_list = []
        for i in range(1, files_number+1):
            print('--------------------------')
            print(product_type, i)
            print('--------------------------')

            data = nutrition_scraper(product_type, i)
            df_list.append(data)

        data = pd.concat(df_list)

        data.to_csv(cwd + f'/data/final/biedronka_nutrition_{product_type}_all.csv', index=False)
        data.to_excel(cwd + f'/data/final/biedronka_nutrition_{product_type}_all.xlsx', index=False)

        print(data)

        df_prodcut_list.append(data)

    all_data = pd.concat(df_prodcut_list)

    all_data.to_csv(cwd + f'/data/final/biedronka_nutrition_all_product_types.csv', index=False)
    all_data.to_excel(cwd + f'/data/final/biedronka_nutrition_all_product_types.xlsx', index=False)

if __name__ == "__main__":
    scrape_all_products()