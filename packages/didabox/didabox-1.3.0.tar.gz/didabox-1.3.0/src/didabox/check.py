# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : check.py
@Date    : 2023/10/31 18:03:44
@Author  : zhchen
@Desc    : 
"""
import time

import requests

from didabox import DidaBox


class CheckBox(DidaBox):
    def check(self):
        params = {
            'from': str(int(time.time()) * 1000),
        }

        response = requests.get(
            'https://api.dida365.com/api/v2/column',
            params=params, cookies=self.cookies, headers=self.headers)
        return response
