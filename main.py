import requests
from bs4 import BeautifulSoup
from random import choice
import time
from requests.exceptions import TooManyRedirects

def proxies_parse():
    proxies = []
    useragents = open('useragents.TXT').read().split('\n')
    useragent = {'User-Agent': choice(useragents)}
    proxy = {'http': 'http://' + '191.101.39.193:80'}
    # hidemy.name outdated
    request = requests.get('https://hidemy.name/ru/proxy-list/?maxtime=600&type=h&anon=4#list', headers=useragent, proxies=proxy)
    request = request.text
    soup = BeautifulSoup(request, features='html.parser')
    tbody = soup.find('table').find('tbody')
    trs = tbody.find_all('tr')
    for tds in trs:
        td = tds.find_all('td')
        iport = td[0].text + ':' + td[1].text
        proxies.append(iport)
    return proxies

def change_proxy(proxies):
    useragents = open('useragents.TXT').read().split('\n')
    proxy = {'http': 'http://' + proxies.pop(0)}
    useragent = {'User-Agent': choice(useragents)}
    return proxy, useragent

def main():
    proxies = []
    names = open('marketnames.TXT').read().split('\n')
    # proxies = proxies_parse()
    with open('proxies.TXT', 'r') as p:
        proxies.append(p.read())
    proxy, useragent = change_proxy(proxies)
    for i in range(1000):
        try:
            url = choice(names)
            response = requests.get(url, headers=useragent, proxies=proxy, allow_redirects=True)
            j = response.text
            if j == 'null':
                pass
            else:
                print(j)
            try:
                if j == 'null':
                    proxy, useragent = change_proxy(proxies)
                    time.sleep(1)
                    response = requests.get(url, headers=useragent, proxies=proxy, allow_redirects=True)
                    j = response.text
                    if j == 'null':
                        pass
                    else:
                        print(j)
                else:
                    pass
            except TooManyRedirects as e:
                print(f'{url} : {e}')
        except TooManyRedirects as e:
            print(f'{url} : {e}')

if __name__ == '__main__':
    main()