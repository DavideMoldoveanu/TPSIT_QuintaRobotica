import requests

r = requests.get('http://127.0.0.1:5000/api/v1/resources/books/all')

print(r)