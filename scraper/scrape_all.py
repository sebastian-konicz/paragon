from scraper.articles_scraper import articles_scraper

def scrape_all_products():
    # product_types = ['warzywa', 'owoce', 'piekarnia', 'nabial','mieso', 'dania-gotowe', 'napoje', 'mrozone',
    #                  'artykuly-spozywcze', 'drogeria', 'dla-domu', 'dla-dzieci', 'dla-zwierzat']
    product_types = ['warzywa', 'owoce']

    for product_type in product_types:
        articles_scraper(product_type)

if __name__ == "__main__":
    scrape_all_products()