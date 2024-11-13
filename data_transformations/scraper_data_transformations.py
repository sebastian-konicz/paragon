import os
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

    print(df.head(5))


    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

    return df

if __name__ == "__main__":
    data_transformation()
