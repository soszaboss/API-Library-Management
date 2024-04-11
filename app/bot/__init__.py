from app.bot.scarpe import Scarpe
from app.bot.function import file_exists


def scarpe_books_data(path):
    if not file_exists(path):
        print('not file')
        book = Scarpe(path)
        return book.scrape(path)


