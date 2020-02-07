#!/usr/bin/env python3
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from bs4 import BeautifulSoup
import re
import requests
import html
import rfc6266

def fetch_url(until=1):
    links = []
    url = 'http://approvedtx.blogspot.tw/'

    try:
        while True:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            segs = soup.findAll('div', class_='post-body entry-content')
            titles = soup.findAll('h3', class_='post-title entry-title')

            for seg, title in zip(segs, titles):
                try:
                    num = re.match('^#([0-9]+)\..*', title.a.string).group(1)
                    # cannot use smaller than, because there's some revised version
                    if int(num) == until:
                        return links

                    href = seg.a.findNext('a')['href'] # it's in the second a
                    links.append(href.strip())
                    print(f'[INFO] Fetched {num}. {seg.b.text}')

                except Exception as e:
                    print(e)
                    continue

            url = soup.findAll('a', class_='blog-pager-older-link')[0]['href']

    except Exception as e:
        print(e)

    return links

def translate_url(url):
    try:
        res = requests.get(url)
        matched = re.search('url=(https://onedrive.live.com/.*) />', res.text)
        next_url = html.unescape(matched.group(1))
        parsed = urlparse(next_url)

        query_dict = dict(parse_qsl(parsed.query))
        query_dict['authkey'] = query_dict['authkey'][1:-1] # to download contents, we must strip ! and " (idk why)
        query_dict['resid'] = query_dict['id']
        del query_dict['id']

        query_string = urlencode(query_dict)

        return urlunparse((parsed[0], parsed[1], '/download', parsed[3], query_string, parsed[5]))

    except Exception as e:
        print(e)
        return None

def download_url(url, counter):
    try:
        res = requests.get(url)
        filename = rfc6266.parse_headers(res.headers['Content-Disposition']).filename_unsafe
        if not filename:
            filename = f'{counter}.zip'

        print(f'[INFO] Get filename {filename}')

        with open(f'download_files/{filename}', 'wb+') as f:
            f.write(res.content)

    except Exception as e:
        print(e)


download_links = fetch_url(until=505)
with open('approvedtx.out', 'w+') as f:
    f.write('\n'.join(download_links))

for i, url in enumerate(download_links):
    url = url.strip()
    print(f'[INFO] Downloading from {url}')

    url = translate_url(url)

    if not url:
        print(f'[ERROR] Translating URL failed: {url}')
    else:
        download_url(url, i)

