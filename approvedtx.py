#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'http://approvedtx.blogspot.tw/'
links = []

while(1):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        segs = soup.findAll('div', class_='post-body entry-content')

        for seg in segs:
            try:
                href = seg.a.findNext('a')['href'] # it's in the second a
            except:
                continue
            links.append(href.strip())
            print('Fetched: ', seg.b.text)

        url = soup.findAll('a', class_='blog-pager-older-link')[0]['href']

    except Exception as e:
        print(e)
        break

with open('approvedtx_out', 'w+') as f:
    f.writelines('\n'.join(links))

