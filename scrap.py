import requests
from bs4 import BeautifulSoup
import json

base_url = 'http://quotes.toscrape.com'
page_number = 1

quotes = []
authors = {}

while True:
    url = f'{base_url}/page/{page_number}/'
    response = requests.get(url)
    
    if response.status_code != 200:
        break
    
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_to_scrape = soup.find_all('div', class_='quote')
    for quote in quotes_to_scrape:
        quote_text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = quote.find('meta', itemprop='keywords')['content'].split(',')

        quotes.append({
            'tags': tags,
            'author': author,
            'quote': quote_text            
        })

        if author not in authors:
            author_url = base_url + quote.find('a')['href']
            authors[author] = author_url

    next_page = soup.find('li', class_='next')
    if next_page:
        page_number += 1
    else:
        break

with open('quotes.json', 'w', encoding='utf-8') as file:
    json.dump(quotes, file, ensure_ascii=False, indent=4)


authors_data = []

for author, author_url in authors.items():
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    born_date = soup.find('span', class_='author-born-date').get_text()
    born_location = soup.find('span', class_='author-born-location').get_text()
    description = soup.find('div', class_='author-description').get_text(strip=True)

    authors_data.append({
        'fullname': author,
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    })

with open('authors.json', 'w', encoding='utf-8') as file:
    json.dump(authors_data, file, ensure_ascii=False, indent=4)
