import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


parser = argparse.ArgumentParser(
    description='Программа сокращает переданную в качестве аргумента \
        ссылку или считает количество переходов по сокращенной ссылке'
)
parser.add_argument('url', help='Полная ссылка или битлинк')
args = parser.parse_args()

load_dotenv()

SHORT_LINK_API = 'https://api-ssl.bitly.com/v4/shorten'
COUNT_CLICKS_API = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
GET_INFO_API = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
TOKEN = os.getenv('BITLY_TOKEN')


def shorten_link(token, url):
    headers = {'Authorization': token}
    payload = {'long_url': url}
    response = requests.post(SHORT_LINK_API, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, url):
    headers = {'Authorization': token}
    params = {'units': '-1'}
    bitlink = urlparse(url).netloc + urlparse(url).path
    response = requests.get(COUNT_CLICKS_API.format(bitlink),
                            headers=headers, params=params)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def check_bitlink(token, url):
    headers = {'Authorization': token}
    bitlink = urlparse(url).netloc + urlparse(url).path
    response = requests.get(GET_INFO_API.format(bitlink), headers=headers)
    return response.ok


def main():
    if TOKEN:
        url = args.url
        if check_bitlink(TOKEN, url):
            try:
                clicks_count = count_clicks(TOKEN, url)
            except requests.exceptions.HTTPError:
                print('Ошибка в URL битлинка')
            else:
                print('Количество переходов:', clicks_count)
        else:
            try:
                bitlink = shorten_link(TOKEN, url)
            except requests.exceptions.HTTPError:
                print('Ошибка в URL')
            else:
                print('Битлинк', bitlink)
    else:
        raise Exception("Отсутствует токен")


if __name__ == "__main__":
    main()
