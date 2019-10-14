import requests
from bs4 import BeautifulSoup
from random import choice
import csv


def get_proxy():
    url = "https://www.sslproxies.org/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')
    return {'https': choice(list(map(lambda x: x[0] + ':' + x[1], list(zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(
        lambda x: x.text, soup.findAll('td')[1::8]))))))}


def proxy_request(request_type, url, **kwargs):
    while 1:
        try:
            proxy = get_proxy()
            r = requests.request(
                request_type, url, proxies=proxy, timeout=5, **kwargs)
            break
        except:
            pass
    return r


csv_file = open('d.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Area', 'Number', 'Link'])

for i in range(1, 52):
    url = 'http://boadiversao.com.br/guia/rio-de-janeiro/bares/locais/p/{}'.format(
        i)

    re = proxy_request('get', url)
    soup = BeautifulSoup(re.text, 'lxml')
    for box in soup.findAll('li', class_='destaque'):
        data = box.find('div', class_='info')
        link = data.a['href']
        name = data.a['title']
        area = data.find('p', class_="data").text
        number = data.find('p', class_='local').text

        print(name, area, number, link, sep='\n')
        print()
        csv_writer.writerow([name, area, number, link])

csv_file.close()
