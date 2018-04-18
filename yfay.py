import os
import json
import requests


YKB_OAUTH2_ENDPOINT = 'https://api.yapikredi.com.tr/auth/oauth/v2/token'
YKB_FUND_ENDPOINT = 'https://api.yapikredi.com.tr/api/calculation/v1/fundInformation'
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')

YKB_API_AUTH = {
    'client_id': os.getenv('YKB_CLIENT_ID'),
    'client_secret': os.getenv('YKB_CLIENT_SECRET'),
    'grant_type': 'client_credentials',
    'scope': 'oob'
}


def get_access_token():
    r = requests.post(YKB_OAUTH2_ENDPOINT, data=YKB_API_AUTH)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    return r.json()


def get_funds():
    token = get_access_token()
    headers = {'Authorization': f'{token["token_type"]} {token["access_token"]}'}
    r = requests.get(YKB_FUND_ENDPOINT, headers=headers)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    return r.json()['response']['return']['fundItemDtoList']


def get_yfay_price():
    funds = get_funds()
    for fund in funds:
        if fund['fundcode'] == 'YFAY1':
            return fund['fundprice']


def post_to_slack(price):
    r = requests.post(SLACK_WEBHOOK, json={'text': f'Bugün itibariyle YFAY1 {price} TL'})
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    return


if __name__ == '__main__':
    price = get_yfay_price()
    post_to_slack(price)
    exit()
