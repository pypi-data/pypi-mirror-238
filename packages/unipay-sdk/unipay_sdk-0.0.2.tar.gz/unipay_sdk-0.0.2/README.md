# unipay-sdk
Python SDK for unipay.com payments gateway

## Install
```shell
pip3 install unipay-sdk
```

## How to ...
### Create order
```python
from unipay_sdk import UniPayClient
from unipay_sdk import OrderItem

client = UniPayClient(
    secretkey='mySecretKeyFromUniPay',
    merchant_id=00000000000000,
    success_url='/url/success',
    cancel_url='/url/cancel',
    callback_url='/url/callback'
)

new_order = client.create_order(
    merchant_order_id='ORDER1234', # Unique order id
    merchant_order_user='1', # User id on merchant side
    order_price=15.35, # in GEL
    order_name='Purchase on example.com',
    order_description='Some description',
    items=[
        OrderItem.from_dict({'price': 7.0, 'quantity': 1, 'title': 'Coffee', 'description': 'Cup of coffee'}),
        OrderItem.from_dict({'price': 8.35, 'quantity': 1, 'title': 'Cake', 'description': 'Big cake'})        
    ]
)
checkout_link = new_order.data.Checkout
order_hash = new_order.data.UnipayOrderHashID
```
### Handle errors
```python
from unipay_sdk import UniPayClient
from unipay_sdk import OrderItem
from unipay_sdk import APIError

client = UniPayClient(...)

new_order = client.create_order(...)

match new_order.errorcode:
    case APIError.OK:
        print('OK')
    case APIError.FREQUENCY_LIMIT_EXCEEDED:
        print('Rate limited')
    # etc...
```

### Test server
To test order workflows you may use [unipay-test-server](https://github.com/BeyondUnderstanding/unipay-test-server)

To use test server you might initialize `UniPayClient` with `test` flag 
```python
from unipay_sdk import UniPayClient

test_client = UniPayClient(..., test=True, test_url='http://localhost:8080')
# test_url is path to unipay-test-server 
```

### Validate
UniPay-SDK also provides Pydantic 2.0 schemas for callbacks and responses
```python
from unipay_sdk.pydantic import BasicUniPayCallback
from unipay_sdk.pydantic import BasicUniPayResponse
```

## Found error or want to contribute?
### You may create a pull request to repository 

