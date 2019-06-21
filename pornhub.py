#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:xxx time:2019/6/19
import requests
url = "https://www.pornhubselect.com/"

import requests

response = requests.get(url, proxies={
    'http': 'http://127.0.0.1:1080',
    'https': 'https://127.0.0.1:1080'
})

print(response.text)