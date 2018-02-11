#!/usr/bin/env python3
import requests
import traceback
from bs4 import BeautifulSoup

url = 'http://kattanagahaha.blog.fc2.com/category2-0.html'
links = []

while True:
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        songs = soup.findAll('td', style='text-align: center;') # missing the final one with div tag
        for song in songs:
            links.append(song.a['href'])
            print('Fetched :', song.a.next_sibling)

        url = soup.findAll('li', class_='next')[0].a['href']

    except:
        traceback.print_exc()
        break

with open('kattanagahaha_out', 'w+') as f:
    f.writelines('\n'.join(links))
