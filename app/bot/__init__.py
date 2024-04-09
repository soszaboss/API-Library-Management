from scarpe import Scarpe
from function import file_exists


def scarpe_books_data():
    path = "../data/books.json"
    if not file_exists(path):
        book = Scarpe("../data/books.json")
        return book.scrape()


scarpe_books_data()
