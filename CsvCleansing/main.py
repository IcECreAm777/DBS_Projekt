import csv
import json

with open('countries.json', encoding='utf-8') as f:
    j = json.load(f)
    countries = []
    for row in j:
        countries.append(row['name'].upper())


# old country names
countries.append("Czechoslovakia".upper())


with open('gdp.csv', newline='') as csvFile:
    reader = csv.reader(csvFile, delimiter=',')
    newCsv = []
    for row in reader:
        newRow = []
        if row[0].upper() not in countries:
            continue

        for i in range(len(row)):
            if i == 2 or i == 3 or i == len(row)-1:
                continue

            if row[i] == '':
                if i-1 > 3 and row[i-1] != '' and i+1 < len(row) and row[i+1] != '':
                    row[i] = (float(row[i-1]) + float(row[i+1])) / 2
                    print("closed gap {} {} {}".format(row[i-1], row[i], row[i+1]))
            newRow.append(row[i])
        newCsv.append(newRow)

    for row in newCsv:
        print(row)
    print(len(newCsv))


continents = {"Asia and Pacific (other)", "EU-28", "Americas (other)", "Africa", "World"}
