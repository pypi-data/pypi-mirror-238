# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : __init__.py
@Date    : 2023/10/31 13:35:24
@Author  : zhchen
@Desc    : 
"""
import random
import string
from datetime import datetime

import pytz


class DidaBox:
    def __init__(self, cookies: dict, headers=None):
        self.headers = headers or {
            'authority': 'api.dida365.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json;charset=UTF-8',
            'hl': 'zh_CN',
            'origin': 'https://dida365.com',
            'pragma': 'no-cache',
            'referer': 'https://dida365.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-tz': 'Asia/Shanghai',
        }
        self.cookies = cookies

        self.tz = 'Asia/Shanghai'

    @staticmethod
    def random_str(num=24) -> str:
        # 16进制字符集
        hex_chars = string.hexdigits[:-6]  # 去除字母大小写重复部分
        # 生成随机的16进制字符串
        random_hex_string = ''.join(random.choice(hex_chars) for _ in range(num))
        return random_hex_string

    @staticmethod
    def random_int(num=13) -> int:
        # 生成一个13位随机数字
        random_number = ''.join(str(random.randint(0, 9)) for _ in range(num))
        return int(random_number)

    def shanghai2utc(self, _date: str) -> str:
        """上海时区转成utc时区"""
        dt = datetime.fromisoformat(_date)
        original_timezone = pytz.timezone(self.tz)
        dt = original_timezone.localize(dt)
        target_timezone = pytz.timezone('UTC')
        converted_time = dt.astimezone(target_timezone)
        return converted_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    @staticmethod
    def utc2str(_date: str) -> str:
        """[%Y-%m-%dT%H:%M:%S.%f%z]格式转成[%Y-%m-%d %H:%M:%S]格式"""
        dt = datetime.fromisoformat(_date)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def str2utc(_date: str) -> str:
        """[%Y-%m-%d %H:%M:%S]格式转成[%Y-%m-%dT%H:%M:%S.%f%z]格式"""
        dt = datetime.strptime(_date, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    @staticmethod
    def now():
        now = datetime.now()
        return now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
