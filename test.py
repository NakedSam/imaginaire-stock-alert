#Increase max number by one
for number in range(1, 3):
    link = "https://imaginaire.com/fr/librairie/oshi-no-ko-v-f-"
    numberToAdd = ""

    if number < 10:
        numberToAdd = numberToAdd + "0"

    numberToAdd = numberToAdd + str(number)

    linkToAdd = link + str(numberToAdd) + ".html"
    
    with open("toCopy.txt", "a", encoding="utf-8") as f:
        opening = ",\n{\n"
        title = '\t"title": "Oshi no Ko",\n'
        volume = f'\t"volume": {str(number)},\n'
        imaginaireLink = '\t"link" : "' + linkToAdd + '"' + "\n"
        ending = "}"
        
        blockToWrite = opening + title + volume + imaginaireLink + ending

        f.write(blockToWrite)