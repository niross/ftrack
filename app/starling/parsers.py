
class StarlingWebhookParser:
    def __init__(self, webhook_content):
        self.trans_type = webhook_content['webhookType']
        self.content = webhook_content['content']

    def parse(self):
        if hasattr(self, '_parse_' + self.trans_type.lower()):
            return getattr(self, '_parse_' + self.trans_type.lower())
        raise NotImplementedError('No parser exists for type {}'.format(self.trans_type))

    def _parse_transaction_card(self):
        return {
            'transaction_uid': self.content['transactionUid'],
            'amount': self.content['amount'],
            'transaction_type': self.content['type'],
            'payee': self.content['counterParty'],
        }
