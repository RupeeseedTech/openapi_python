# openapi_python
OpenAPI-PYTHON is a Python library for interacting with Trading platform ,that is a set of REST-like HTTP APIs that expose many capabilities required to build stock market investment and trading platforms. It lets you execute orders in real time..

# Installation
Use the package manager pip to install smartapi-python.

```
pip install -r req.txt       # for downloading the other required packages
```

# Usage
```python
# package import statement
from OpenAPI import APIConnect

# defining the api-endpoint
API_ENDPOINT = "YOUR_ENDPOINT"
SOURCE="M" # M - Mobile / W - Web 
CLIENT_ID="YOUR_ID"
TOKEN = "Access token generated from Website"

openapi = APIConnect(API_ENDPOINT,CLIENT_ID,SOURCE,TOKEN)

#place order
data = {'transaction_type':'Buy',
        'exchange_segment':'BSEEQ',
        'product':'MARGIN',
        'security_id':'532540',
        'quantity':'1',
        'price':'3200',
        'validity':'DAY',
        'disc_quantity':'',
        'trigger_price':'',
        'offline_order':'false'}
response = openapi.place_order(data)
print('place order api response --> ',response)


#fetch orderbook
data = openapi.orderbook()
print("orderbook data====",data)

#modify order
data = { 'order_id':'order_no',
        'quantity':'2',
        'price':'3200',
        'validity':'DAY',
        'disc_quantity':'',
        'trigger_price':'',
        'offline_order':'false'}

response = openapi.modify_order(data)
print('modify order api response --> ',response)


#cancel order
data = { 'order_id':'order_no fetched from orderbook'}

response = openapi.cancel_order(data)
print('cancel order api response --> ',response)

```
