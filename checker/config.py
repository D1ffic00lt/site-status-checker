# -*- coding:utf-8 -*-
FORMAT = '[%(asctime)s] [%(levelname)s]: %(message)s'
DATE_FORMAT = "[%Y-%m-%d %H:%M:%S]"
LOG_PATH = "logs.log"

IP = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]" \
     r"|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4]" \
     r"[0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|" \
     r"[01]?[0-9][0-9]?)"

headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
