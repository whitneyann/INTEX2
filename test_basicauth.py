import requests

response = requests.get('http://localhost:8000/catalog/search/', auth=('maya@roney.com', 'mayaroney8'),params={
    #'page': 1,
    'name': 'Couch',
    'category': 'Software',
    'maxprice': 500.00,
})

print('Status code', response.status_code)
print(response.json())
