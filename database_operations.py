# This file is a collection of all needed database queries and operations

import sqlite3
import csv_Cleansing

conn = sqlite3.connect('db/dbs_project.db')
cursor = conn.cursor()


# checks for existing tables and creates them if needed
def init():
    # checks for the Land Table
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Land'").fetchall()
    if not tables:
        cursor.execute('''CREATE TABLE Land 
                            (Code TEXT PRIMARY KEY NOT NULL,
                             Name TEXT NOT NULL);''')
        values_to_insert_countries = csv_Cleansing.getCountries()
        cursor.executemany("INSERT INTO Land(Code, Name) VALUES (?, ?);", values_to_insert_countries)
        conn.commit()

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Temperatur'").fetchall()
    if not tables:
        cursor.execute('''CREATE TABLE Temperatur
                    (Jahr INT NOT NULL,
                    Durchschnittswert FLOAT,
                    land_code TEXT NOT NULL,
                    PRIMARY KEY(Jahr,land_code))''').fetchall()
        # csv_Cleansing.getTemperatureData()
        values_to_insert_temperature_world = csv_Cleansing.getTemperatureWorldData()
        values_to_insert_temperature_countries = csv_Cleansing.getTemperatureData()
        cursor.executemany("insert into Temperatur(Jahr, Durchschnittswert, land_code) VALUES (?, ?, ?);",
                           values_to_insert_temperature_world)
        cursor.executemany("INSERT OR REPLACE INTO Temperatur(Jahr, Durchschnittswert, land_code) VALUES (?, ?, ?);",
                           values_to_insert_temperature_countries)
        conn.commit()

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='GDP'").fetchall()
    if not tables:
        cursor.execute('''CREATE TABLE GDP
                        (Jahr INT NOT NULL,
                        Wert FLOAT,
                        land_code Text NOT NULL,
                        PRIMARY KEY(Jahr, land_code),
                        FOREIGN KEY(land_code) REFERENCES Land(Code))''')
        values_to_insert_gdp = csv_Cleansing.getGdpData()
        cursor.executemany("insert into GDP(Jahr, Wert, land_code) VALUES (?, ?, ?);", values_to_insert_gdp)
        conn.commit()

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Einwohner'").fetchall()
    if not tables:
        cursor.execute('''CREATE TABLE Einwohner
                        (Jahr INT NOT NULL,
                        Anzahl INT,
                        land_code Text NOT NULL,
                        PRIMARY KEY(Jahr,land_code))''')
        values_to_insert_population = csv_Cleansing.getPopulationData()
        cursor.executemany("insert into Einwohner(Jahr, Anzahl, land_code) VALUES (?, ?, ?);",
                           values_to_insert_population)

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Emission'").fetchall()
    if not tables:
        cursor.execute('''CREATE TABLE Emission
                        (Jahr INT NOT NULL,
                        Wert FLOAT,
                        land_code TEXT NOT NULL,
                        PRIMARY KEY(Jahr, land_code),
                        FOREIGN KEY(land_code) REFERENCES Land(Code))''')
        values_to_insert_emission = csv_Cleansing.getEmissionData()
        cursor.executemany("insert into Emission(land_code, Jahr, Wert) VALUES (?, ?, ?);",
                           values_to_insert_emission)
        conn.commit()


# closes the connection to the db
def close():
    conn.close()


# get all the country names
def getCountryNames():
    return cursor.execute('select * from Land;').fetchall()


# gets the temperature, emission, gdp and citizens plot data
def getPlotData(country):
    return getKeyValuePair("Temperatur", "Durchschnittswert", country), \
           getKeyValuePair("Emission", "Wert", country), \
           getKeyValuePair("GDP", "Wert", country), \
           getKeyValuePair("Einwohner", "Anzahl", country)


def getKeyValuePair(table, value_name, country):
    x = []
    y = []
    all_val = cursor.execute("SELECT Jahr, " + value_name + " FROM " + table + " WHERE land_code='" + country + "'") \
        .fetchall()
    for i in range(len(all_val)):
        x.append(all_val[i][0])
        y.append(all_val[i][1])
    return [x, y]


def getLandCodeByName(country_name):
    names = cursor.execute("SELECT Code FROM Land WHERE Name='" + country_name + "'").fetchall()
    return names[0][0] if len(names) > 0 else ''
