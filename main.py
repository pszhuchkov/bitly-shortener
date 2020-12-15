import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


SHORT_LINK_API = 'https://api-ssl.bitly.com/v4/shorten'
COUNT_CLICKS_API = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
GET_INFO_API = 'https://api-ssl.bitly.com/v4/bitlinks/{}'


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
    bitlink = '{}{}'.format(urlparse(url).netloc, urlparse(url).path)
    response = requests.get(COUNT_CLICKS_API.format(bitlink),
                            headers=headers, params=params)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def check_bitlink(token, url):
    headers = {'Authorization': token}
    bitlink = '{}{}'.format(urlparse(url).netloc, urlparse(url).path)
    response = requests.get(GET_INFO_API.format(bitlink), headers=headers)
    return response.ok


def get_parsed_arguments():
    parser = argparse.ArgumentParser(
        description='Программа сокращает переданную в качестве аргумента \
            ссылку или считает количество переходов по сокращенной ссылке'
    )
    parser.add_argument('url', help='Полная ссылка или битлинк')
    return parser.parse_args()


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    args = get_parsed_arguments()
    if check_bitlink(token, args.url):
        try:
            clicks_count = count_clicks(token, args.url)
            print('Количество переходов:', clicks_count)
        except requests.exceptions.HTTPError as error:
            print(error)
    else:
        try:
            bitlink = shorten_link(token, args.url)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError as error:
            print(error)


if __name__ == "__main__":
    main()
