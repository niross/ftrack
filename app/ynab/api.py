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
        return self.session.get(
            BASE_URL + endpoint,
            data=data
        )

    def get_accounts(self):
        return self.get('/budgets/last-used/accounts').json()

    def get_budgets(self):
        return self.get('/budgets').json()

    def create_transaction(self, trans_data):
        self.post('/budgets/last-used/transactions', {
            'transaction': {
                'account_id': 'string',
                'date': 'string',
                'amount': 0,
                'payee_id': 'string',
                'payee_name': 'string',
                'category_id': 'string',
                'memo': 'Added by FTrack',
                'cleared': 'cleared',
                'approved': True,
            }
        })
