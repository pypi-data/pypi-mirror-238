from affliction.base import SynchronousMicrosoftApiClient


class ExchangeClient(SynchronousMicrosoftApiClient):
    def __init__(self, tenant_id=None, client_id=None,
                 client_secret=None, creds=None, base_url=None, scope=None,
                 **kwargs):
        app_url = 'https://outlook.office365.com'
        scope = scope or f'{app_url}/.default'
        base_url = base_url or f'{app_url}/adminApi/beta/{tenant_id}'
        super().__init__(
            tenant_id, client_id, client_secret, creds=creds, base_url=base_url,
            scope=scope,
        )

    def recipients(self, params=None, **kwargs):
        url = f'{self.base_url}/Recipient'
        return list(self.yield_result(url, params=params, **kwargs))

    def mailboxes(self, params=None, **kwargs):
        url = f'{self.base_url}/Mailbox'
        return list(self.yield_result(url, params=params, **kwargs))
