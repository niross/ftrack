import json
from datetime import datetime

import requests


BASE_URL = 'https://api.youneedabudget.com/v1'


class YNABApi:
    def __init__(self, user):
        self.session = requests.session()
        self.session.headers['Authorization'] = 'Bearer {}'.format(user.ynab_auth_code)
        self.user = user

    def get(self, endpoint):
        return self.session.get(BASE_URL + endpoint)

    def post(self, endpoint, data):
        return self.session.post(
            BASE_URL + endpoint,
            json=data
        )

    def get_accounts(self):
        return self.get('/budgets/last-used/accounts').json()

    def get_budgets(self):
        return self.get('/budgets').json()

    def get_categories(self):
        return self.get('/budgets/last-used/categories').json()

    def get_payees(self):
        return self.get('/budgets/last-used/payees').json()

    def get_transactions(self):
        return self.get('/budgets/last-used/transactions').json()

    def create_transaction(self, amount, payee):
        trans_data = {
            'account_id': self.user.ynab_account_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'amount': int(amount * 1000),
            'payee_name': payee,
            'category_id': self.user.ynab_category_id,
            'memo': 'Added by FTrack',
            'approved': True,
        }
        resp = self.post('/budgets/last-used/transactions', {
            'transaction': trans_data
        })
        return resp.json()
