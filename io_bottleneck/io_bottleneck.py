import urllib.request
import time
from bs4 import BeautifulSoup


start = time.time()
request = urllib.request.urlopen('http://www.example.com')
page_html = request.read()
stop_fetching_main_page = time.time()
total_time = stop_fetching_main_page - start
print(f'Total time to fetch the page: {total_time}')

soup = BeautifulSoup(page_html, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))

stop_fetching_all_links = time.time()
print(f'Total execution time: {stop_fetching_all_links - start}')
