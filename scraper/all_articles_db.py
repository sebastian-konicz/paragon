import os
import pandas as pd
from scraper.nutrition_scraper import nutrition_scraper

def all_articles_db():
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
            file_path = cwd +f'/data/raw/{product_type}/biedronka_items_{product_type}_{i}.csv'
            data = pd.read_csv(file_path)
            data['item_id'] = data['item_id'].apply(lambda x: str(x).zfill(10))
            df_list.append(data)

        data = pd.concat(df_list)

        data.to_csv(cwd + f'/data/interim/articles_db/biedronka_{product_type}_all.csv', index=False)
        data.to_excel(cwd + f'/data/interim/articles_db/biedronka_{product_type}_all.xlsx')

        print(data)

        df_prodcut_list.append(data)

    all_data = pd.concat(df_prodcut_list)

    all_data.to_csv(cwd + f'/data/interim/articles_db/biedronka_all_product_types.csv', index=False)
    all_data.to_excel(cwd + f'/data/interim/articles_db/biedronka_all_product_types.xlsx', index=False)

if __name__ == "__main__":
    all_articles_db()