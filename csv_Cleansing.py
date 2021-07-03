import csv
import database_operations as db

# initialization stuff
with open('data/countries.csv', encoding='utf-8') as f:
    c = csv.reader(f, delimiter=',')
    countries = []
    for c_row in c:
        countries.append(c_row[0].upper())


# old country names
countries.append("Czechoslovakia".upper())
# a list of 'continents' used for filtering
continents = {"Asia and Pacific (other)", "EU-28", "Americas (other)", "Africa", "OWID_WRL"}


def getCountries():
    with open('data/countries.csv', encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        new_csv = []
        for row in reader:
            new_row = [row[1], row[0]]
            new_csv.append(new_row)
    new_csv.pop(0)
    return new_csv


def getGdpData():
    with open('data/gdp.csv', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        new_csv = []
        for row in reader:
            new_row = []
            if row[0].upper() not in countries:
                continue
    
            for i in range(len(row)):
                if i == 0 or i == 2 or i == 3 or i == len(row)-1:
                    continue
                new_row.append(row[i])
            new_csv.append(new_row)

    ordered_csv = []
    for row in range(len(new_csv)):
        for j in range(61):
            if new_csv[row][1+j] == '':
                continue
            ordered_csv.append([1960+j, float(new_csv[row][1+j]), new_csv[row][0]])

    #new_csv.pop(0)
    return ordered_csv


def getEmissionData():
    with open('data/co2_emission.csv', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        new_csv = []
        for row in reader:
            new_row = []
            if row[0].upper() not in countries and row[0].upper() not in continents:
                continue
            for i in range(len(row)):
                if i == 0:
                    continue
                new_row.append(row[i])
                if row[1] == '':                # why pattern match no work???
                    if row[0] == 'Africa':
                        new_row[0] = 'AFRK'
                    if row[0] == 'EU-28':
                        new_row[0] = 'EU28'
                    if row[0] == 'Americas (other)':
                        new_row[0] = 'USNA'
                    if row[0] == 'Asia and Pacific (other)':
                        new_row[0] = 'ASAP'
            new_csv.append(new_row)
    #new_csv.pop(0)
    return new_csv


def getTemperatureData():
    with open('data/GlobalLandTemperaturesByCountry.csv', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        new_csv = []
        for row in reader:
            new_row = []
            if row[3].upper() not in countries and row[3].upper() not in continents:
                continue
            for i in range(len(row)):
                if i == 2:
                    continue
                new_row.append(row[i])
            new_csv.append(new_row)

    year_csv = []
    i = 1
    temperatures = []
    while 1:
        if new_csv[i][0][0:4] == '2013' and new_csv[i][2] == 'Zimbabwe':
            break
        if new_csv[i][0][0:4] != new_csv[i-1][0][0:4]:
            temperatures = []

        if new_csv[i][1] == '':
            i += 1
            continue
        temperatures.append(float(new_csv[i][1]))

        if len(temperatures) == 12:
            year_csv.append([new_csv[i][0][0:4], sum(temperatures)/12, db.getLandCodeByName(new_csv[i][2])])
            temperatures = []

        i += 1

    return year_csv


def getTemperatureWorldData():
    with open('data/GlobalTemperatures.csv', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        new_csv = []
        for row in reader:
            new_row = []
            for i in range(len(row)):
                if i > 1:
                    break
                new_row.append(row[i])
            new_row.append('WORLD')
            new_csv.append(new_row)

    year_csv = []
    i = 1
    temperatures = []
    while 1:
        if new_csv[i][0][0:4] != new_csv[i-1][0][0:4]:
            temperatures = []

        if new_csv[i][1] == '':
            i += 1
            continue
        temperatures.append(float(new_csv[i][1]))

        if len(temperatures) == 12:
            year_csv.append([new_csv[i][0][0:4], sum(temperatures)/12, 'OWID_WRL'])
            temperatures = []

        if new_csv[i][0][0:7] == '2015-12':
            break

        i += 1

    return year_csv


def getPopulationData():
    with open('data/population_total.csv', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        new_csv = []
        for row in reader:
            if row[0].upper() not in countries and row[0].upper() not in continents:
                continue

            new_csv.append([row[1], row[2], db.getLandCodeByName(row[0])])
    #new_csv.pop(0)
    return new_csv
