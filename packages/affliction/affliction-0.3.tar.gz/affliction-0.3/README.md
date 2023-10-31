# affliction

welcome to affliction.  provides synchronous clients, based on deceit,
for interacting with the microsoft graph api and the exchange management 
rest api.  please be mindful that the exchange rest api is (still, as of 2023
after more than three years) in beta, and these apis are not currently published.   
this means that the exchange rest api will likely change between the time
that this library is published and the time the exchange management rest api
is officially released.

powered by angry penguins.  


# graph client

to use the graph client, you use the `affliction.graph_client.SynchronousGraphClient`
class.  there are a few pre-defined endpoints for now for `users` and 
`subscribedSkus`.  

```python
from affliction.graph_client import SynchronousGraphClient
client = SynchronousGraphClient(
    tenant_id='01234567-000...',
    client_id='01234567-000...',
    client_secret='secret generated from azure app registration',
)
users = client.get_users(params={
    '$search': '"displayName:alice"',
})
```

documentation for the [users endpoint](https://learn.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http)
is available from micrososft.  other documents provide a more fulsome 
description of the [available odata parameters](https://learn.microsoft.com/en-us/graph/query-parameters?tabs=http)


# exchange client

to use the exchange client, instantiate `affliction.exchange_client.ExchangeClient`

use the mailboxes endpoint with `$filter` or `$search` odata semantics just 
like you would with the graph api.

```python
from affliction.exchange_client import ExchangeClient
client = ExchangeClient(
    tenant_id='01234567-00...',
    client_id='01234567-00...',
    client_secret='app secret from azure app registration with Exchange.ManageAsApp permissions'    
)
mailboxes = client.mailboxes(params={
    '$search': '"displayName:catsareawesome"',
})
recipients = client.recipients(params={
    '$filter': 'LitigationHoldEnabled eq True',
})
```

hat tip to Vasil Michev who got us started down this path:  
https://www.michev.info/blog/post/2869/abusing-the-rest-api-endpoints-behind-the-new-exo-cmdlets

to see how to add the required `ManageAsApp` permission, please feel free to 
reference this link: https://4sysops.com/archives/connect-to-exchange-online-with-powershell-and-certificate-based-authentication/
