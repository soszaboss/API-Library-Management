import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import json

class Scarpe:
    def __init__(self, path ):
        self.URL = 'https://openlibrary.org/trending/forever'
        self.data = []
        self.PATH = path

    def soup_func(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 '
                          'Safari/537.36 Edg/123.0.0.0'}
        r = requests.get(url, headers=header)
        return BeautifulSoup(r.text, 'lxml')

    def pretiffy(self, soup):
        return soup.prettify()

    def xpath(self, soup, path):
        return etree.HTML(str(soup)).xpath(path)[0].text

    def clean_data(self, path: str, data: list):
        file = json.dumps(data)
        data = pd.read_json(file, convert_dates=['publication_date'])
        data['page'] = data['page'].astype(str)
        data['page'] = data['page'].str.replace('nan', 'Unknown')
        data['page'] = data['page'].apply(lambda x: x[:-2:] if x != 'Unknown' else x)
        data['language'] = data['language'].apply(lambda x: 'Unknown' if x == '' else x)
        data['genre'] = data['genre'].apply(lambda x: ', '.join(x))
        data['image'] = data['image'].apply(lambda x: 'https:' + x if x.startswith('//') else x)
        with open(path, 'w') as f:
            new_data = data.to_dict(orient='records')
            json.dump(new_data, f, indent=4)
    def pagination_pages(self):
        soup = self.soup_func(self.URL)
        # pagination list pages
        pagination_links = [link['href'] for link in soup.find_all('a', attrs={'class': 'ChoosePage'})][:-1:]
        return ['/trending/forever?page=1'] + pagination_links

    def scrape(self):
        pagination_links = self.pagination_pages()
        for pagination_link in pagination_links:

            url = f"https://openlibrary.org{pagination_link}"

            # scarpe the actual pagination link page
            pagination_soup = self.soup_func(url)

            # get the list of books of this actual page
            list_group = pagination_soup.find_all('li', attrs={'class': 'searchResultItem'})

            # get the link detail page of every book
            links_detail_book_page = [link.find('a', attrs={'itemprop': 'url'})['href'] for link in list_group]
            for books_detail in links_detail_book_page:
                new_url = f"https://openlibrary.org{books_detail}"
                # book_detail = requests.get(new_url)
                new_soup = self.soup_func(new_url)  # BeautifulSoup(book_detail.text, 'html.parser')
                publishers = [publisher.text for publisher in new_soup.find_all('a', attrs={'itemprop': 'publisher'})]
                try:
                    isbn = [isbn.text for isbn in
                            new_soup.find_all('dd', attrs={'class': 'object', 'itemprop': 'isbn'})]
                    isbn10 = isbn[0]
                    isbn15 = isbn[1]
                except:
                    isbn10 = None
                    isbn15 = None
                try:
                    page = new_soup.find('span', attrs={'class': 'edition-pages', 'itemprop': 'numberOfPages'}).text
                except:
                    page = None
                try:
                    language = [language.a.text for language in
                                new_soup.find_all('span', attrs={'itemprop': 'inLanguage'})]
                except ValueError:
                    language = None
                try:
                    title = new_soup.find('h1', attrs={'class': 'work-title', 'itemprop': 'name'}).text
                except:
                    title = None
                book_data = {
                    'title': title,
                    'author': new_soup.find('a', attrs={'itemprop': 'author'}).text,
                    # xpath(new_soup, '//*[@id="contentBody"]/div[1]/div[3]/div[2]/span/h2[2]/a'),
                    'publication_date': self.xpath(new_soup, '//*[@id="contentBody"]/div[1]/div[3]/div[5]/div/div[1]/span'),
                    'page': page,
                    'language': ' '.join(language),
                    'publishers': f"{', '.join(publishers)}",
                    'description': self.xpath(new_soup, '//*[@id="contentBody"]/div[1]/div[3]/div[4]/div/p[1]'),
                    'isbn10': isbn10,  # xpath(new_soup, '//*[@id="contentBody"]/div[1]/div[3]/div[9]/div[4]/dl/dd[4]'),
                    'isbn15': isbn15,
                    'image': new_soup.find('img', attrs={'itemprop': 'image'})['src'],
                    'genre': [a.text for a in
                              new_soup.find_all('a', attrs={'data-ol-link-track': "BookOverview|SubjectClick"})]
                }
                # print(book_data)
                self.data.append(book_data)

        return self.clean_data(self.PATH, self.data)
