# Account to card implementation with Universal bank

Support Group - <a href="https://t.me/+Ng1axYLNyBAyYTRi">Telegram</a> <br/>

## Installation

```shell
pip install ubk-pkg
```

### Test-Credentials

```
Card Numer: 8600 4829 5296 4119
Card Numer: 9860 2301 0122 3272
```

## Documentation
- [Account2Card](#account2card)
- [StatusCheck](#statuscheck)
- [CancelCheck](#cancelcheck)

# Methods

## Account2Card

```python
from pprint import pprint

from ubk.client import UniPosAPI
from ubk.types.http import rpc_request


ubk_client = UniPosAPI(
    url="api-url",
    token="access-token"
)

resp_data = ubk_client.account2card(
    params=rpc_request.Account2Card(
        number="8600482952964119",
        amount="17.00",
    )
)

pprint(resp_data)
```

## StatusCheck

```python
from pprint import pprint

from ubk.client import UniPosAPI
from ubk.types.request import RequestTransferCreditState


ubk_client = UniPosAPI(
    url="api-url",
    token="access-token"
)

resp_data = ubk_client.status_check(
    params=rpc_request.State(
        ext_id="576d2529-5556-4ceb-b3ca-25cab475b57a"
    )
)

pprint(resp_data)
```

## CancelCheck

```python
from pprint import pprint

from ubk.client import UniPosAPI
from ubk.types.request import RequestTransferCreditCancel


ubk_client = UniPosAPI(
    url="api-url",
    token="access-token"
)

resp_data = ubk_client.cancel_check(
    params=rpc_request.Cancel(
        ext_id="576d2529-5556-4ceb-b3ca-25cab475b57a"
    )
)

pprint(resp_data)

```