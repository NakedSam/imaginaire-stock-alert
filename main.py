from encodings import utf_8
from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import datetime

with open("list.json", "r", encoding="utf_8") as f:
    mangas = json.load(f)

with open("log.txt", "r", encoding="utf_8") as f:
    logEntries = f.readlines()

mangasList = mangas.copy()
mostRecentEntry = []

class Manga:
    def __init__(self, title, status, volume, link=None):
        self.title = title
        self.status = status
        self.volume = volume
        self.link = link

    def __str__(self):
        return f"title : {self.title} volume : {self.volume} status : {self.status}"

def inList(title, volume):
    for manga in mostRecentEntry:
        if manga.title == title and int(manga.volume) == volume:
            return True
    return False

def getStatus(title, volume):
    for manga in mostRecentEntry:
        if manga.title == title and int(manga.volume) == volume:
            return manga.status
    return None

#GÉNÉRATION AUTOMATIQUE DE LIENS
for entry in reversed(logEntries):
    status = ""
    title = ""
    volume = None

    #Get the date
    dateREString = "(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{6})"
    entryDate = re.match(dateREString, entry).group()
    #Remove it
    entryDateLessString = entry.replace(entryDate, "").strip()
    #Get the title
    titleREString = "^.{1,}(?= v\.\d{1,5} : (DISPO|INDISPONIBLE))"

    try:
        title = re.search(titleREString, entryDateLessString).group()
        volume = re.search("(?!^.{1,} v\.)\d{1,5}(?= : (DISPO|INDISPONIBLE))", entryDateLessString).group()
        status = re.search("(?!^.{1,} )(?!v\.\d{1,5})(?! : )(DISPO|INDISPONIBLE)", entryDateLessString).group()
        
        mangaToAdd = Manga(title=title, status=status, volume=volume)
        #We can add the manga safely if the list is empty
        if len(mostRecentEntry) == 0:
            mostRecentEntry.append(mangaToAdd)
        #Else we check if the volume of manga is already in it, if not, we add it to the most recent entry list
        else:
            isInMangaList = False
            isInMangaList = [True for manga in mostRecentEntry if manga.title ==  title and manga.volume == volume]

            if not isInMangaList:
                mostRecentEntry.append(mangaToAdd)

    except Exception as e:
        print(e)
        pass


for manga in mangas:
    page = requests.get(manga["link"]).text
    soup = BeautifulSoup(page, "lxml")
            

    links = soup.find_all(class_="rewards__product-points")
    stringToWrite = f"{manga['title']} v.{manga['volume']} : "
    #Check if the manga is already in the log file
    isInMangaList = inList(manga["title"], manga["volume"])
    #We get the previousStatus from the log file
    previousStatus = None

    if isInMangaList:    
        previousStatus = getStatus(manga["title"], manga["volume"])
           
    if len(links) > 0:
        stringToWrite = f"{datetime.now()} " + stringToWrite + f"DISPO {manga['link']}"

        if previousStatus == "INDISPONIBLE":
            stringToWrite = stringToWrite + "NOUVEAU"

        stringToWrite = stringToWrite + "\n"
        print(stringToWrite)
    else:
        stringToWrite = f"{datetime.now()} " + stringToWrite + f"INDISPONIBLE"

        if previousStatus == "DISPO":
            stringToWrite = stringToWrite + "NOUVEAU"

        stringToWrite = stringToWrite + "\n"
        print(stringToWrite)

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(stringToWrite)