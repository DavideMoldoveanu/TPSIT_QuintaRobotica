import requests
import json


while True:
    print("1 - Stampa casuale\n2 - Stampa le categoria\n3 - Stampa per categoria\n4 - Stampa per nome\n5 - Esci")
    cat = int(input("Inserisci tipologia di stampa: "))

    print("")

    if cat == 1:
        url = "https://api.chucknorris.io/jokes/random"
        x = requests.get(url)
        jsonPrint = x.json()
        jsonPrint = jsonPrint["value"]
        print(jsonPrint)
        print("")
    elif cat == 2:
        url = "https://api.chucknorris.io/jokes/categories"
        x = requests.get(url)
        print(x.text)
        print("")
    elif cat == 3:
        categoria = input("Inserisci categoria: ")
        url = f"https://api.chucknorris.io/jokes/random?category={categoria}"
        x = requests.get(url)
        jsonPrint = x.json()
        jsonPrint = jsonPrint["value"]
        print(jsonPrint)
        print("")
    elif cat == 4:
        query = input("Inserisci parola: ")
        url = f"https://api.chucknorris.io/jokes/search?query={query}"
        x = requests.get(url)
        for k in json.loads(x.text)['result']:
            print(k['value'])
            print("")
        print("")
    else:
        break
