from bs4 import BeautifulSoup
import requests
import re
import json

data = None

with open("list.json", "r") as f:
    mangas = json.load(f)

for manga in mangas:
    page = requests.get(manga["link"]).text
    soup = BeautifulSoup(page, "lxml")
            

    links = soup.find_all(class_="rewards__product-points")

    if len(links) > 0:
        print(f"{manga['title']} v.{manga['volume']} : DISPO {manga['link']}")
    else:
       print(f"{manga['title']} v.{manga['volume']} : INSDISPONIBLE")