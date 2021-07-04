#
# DBS Project - ue10
# Henning Gütschow
# Niklas Rosseck
# Kilian Woick
#

import database_operations as db
from appJar import gui

# initialize UI
app = gui("DBS Project - Data Visualization", "1300x1000", showIcon=False)
# initialize database
db.init()


# gets the temperature, emission, gdp and citizens plot data
def fetchData():
    selected = app.getOptionBox("Countries")
    code = selected.split(',')[0][2:-1]
    country = selected.split(',')[1][2:-2]
    temperatures, emissions, gdp, population = db.getPlotData(code)
    updatePlotFig(temperaturePlot, "Temperatures", temperatures[0], temperatures[1], country)
    updatePlotFig(emissionPlot, "Emissions", emissions[0], emissions[1], country)
    updatePlotFig(gdpPlot, "GDP", gdp[0], gdp[1], country)
    updatePlotFig(populationPlot, "Population", population[0], population[1], country)


def updatePlotFig(plot_figure, title, x_values, y_values, country_name):
    ax = plot_figure.gca()
    ax.plot(x_values, y_values, label=country_name)
    ax.legend()
    app.refreshPlot(title)


def clearData():
    ax = temperaturePlot.gca()
    ax.clear()
    ax.set_title("Temperatures")

    ax = emissionPlot.gca()
    ax.clear()
    ax.set_title("Emissions")

    ax = populationPlot.gca()
    ax.clear()
    ax.set_title("Population")

    ax = gdpPlot.gca()
    ax.clear()
    ax.set_title("GDP")

    app.refreshPlot("Temperatures")
    app.refreshPlot("Emissions")
    app.refreshPlot("Population")
    app.refreshPlot("GDP")


# initialize UI and global variables
app.startScrollPane("MainWindow", sticky="news")

# frame containing interactive UI elements
app.startFrame("interactive", sticky="news")
app.addLabelOptionBox("Countries", db.getCountryNames(), 0, 0)
app.button("fetch", fetchData, 0, 1)
app.button("clear", clearData, 0, 2)
app.stopFrame()

# frame containing all plots
app.startFrame("Plots", sticky="news")
temperaturePlot = app.addPlotFig("Temperatures", 0, 0)
a = temperaturePlot.add_subplot(111)
a.set_title("Temperatures")
a.set_xlabel("Year")
a.set_ylabel("Avg. Temperature")

emissionPlot = app.addPlotFig("Emissions", 0, 1)
a = emissionPlot.add_subplot(111)
a.set_title("Emissions")
a.set_xlabel("Year")
a.set_ylabel("Emissions")

populationPlot = app.addPlotFig("Population", 1, 0)
a = populationPlot.add_subplot(111)
a.set_title("Population")
a.set_xlabel("Year")
a.set_ylabel("Total Num of Citizens")

gdpPlot = app.addPlotFig("GDP", 1, 1)
a = gdpPlot.add_subplot(111)
a.set_title("GDP")
a.set_xlabel("Year")
a.set_ylabel("Value")
app.stopFrame()

app.stopScrollPane()

# open UI
app.go()

# close bd connection
db.close()
