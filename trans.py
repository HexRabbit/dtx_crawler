#!/usr/bin/env python3
import requests
import sys

links = []
modified = []
i = 0

with open(sys.argv[1], 'r') as f:
    links = f.read().split('\n')


for link in links:
    # for onedrive
    if '1drv' in link:
        res = requests.get(link, allow_redirects=False)
        print('Changed: ', i)
        i += 1
        if res.status_code == 301:
            modified.append(res.headers['location'])
            print(res.headers['location'])

with open(sys.argv[1]+'_mod', 'w+') as f:
    f.writelines('\n'.join(modified))

