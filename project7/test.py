from Scraping import *


def main():
    db_name = 'kitaplar.db'
    ws = WebScrapper(db_name)
    ws.parse()

    with shelve.open(db_name, 'r') as db:
        for keys, values in db.items():
            print(keys, ':', values)


if __name__ == '__main__':
    main()
