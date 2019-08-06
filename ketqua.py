#!/usr/bin/env python3

'''
Viết một script kiểm tra xem các số argument đầu vào có trúng lô không
(2 số cuối trùng với một giải nào đó). Nếu không có argument nào thì print
ra tất cả các giải từ đặc biệt -> giải 7.

Lấy kết quả từ ``ketqua.net``.

Dạng của câu lệnh:: 

  ketqua.py [NUMBER1] [NUMBER2] [...]

Các thư viện:

- requests
- requests_html hay beautifulsoup4 [tuỳ chọn]
- argparse hay sys.argv

'''


from bs4 import BeautifulSoup as bs
import sys
import requests
import logging


logger = logging.getLogger(__name__)


def lottery_prize(url):
    r = requests.get(url)
    page = bs(r.text, "html.parser")
    all_prize = (['Đặc biệt', 'Giải nhất', 'Giải nhì', 'Giải ba',
                  'Giải tư', 'Giải năm', 'Giải sáu', 'Giải bảy'])

    result = []

    for i in range(8):
        for j in range(6):
            pid = "rs_{}_{}".format(i, j)
            pnum = page.find(attrs={'id': pid})
            if pnum is not None:
                result.append((all_prize[i], pnum.text))
    return result


def check_prize(input_data):
    data = lottery_prize("https://ketqua.net")
    result = ''
    for prize, lottery in data:
        if int(input_data) == int(lottery[-2:]):
            result = ('Bạn đã trúng {}: {}').format(prize, lottery)
            print(result)
            break

    if result == '':
        print('Chúc bạn may mắn lần sau!')


def main():
    r = requests.get("https://ketqua.net")
    page = bs(r.text, "html.parser")
    tr = page.tbody.find_all("tr")
    td = page.tbody.find("td")

    if len(sys.argv[1]) > 1:
        for i in sys.argv[1:]:
            print('Lô tô:', i)
            check_prize(i)
    print('\nTất cả các giải:')
    for td in tr[:-1]:
        print(td.get_text(separator=' '))


if __name__ == "__main__":
    main()
