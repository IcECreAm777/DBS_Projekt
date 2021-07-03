#
# DBS Project - ue10
# Henning Gütschow
# Niklas Rosseck
# Kilian Woick
#

import database_operations as db
from appJar import gui

# initialize UI
app = gui("DBS Project - Data Visualization", "1080x720", showIcon=False)
# initialize database
db.init()


# gets the temperature, emission, gdp and citizens plot data
def fetchData():
    selected = app.getOptionBox("Countries")
    code = selected.split(',')[0][2:5]
    temperatures, emissions, gdp, population = db.getPlotData(code)
    updatePlotFig(temperaturePlot, "Temperatures", "Year", "Avg. Temperature", temperatures[0], temperatures[1])
    updatePlotFig(emissionPlot, "Emissions", "Year", "Emissions", emissions[0], emissions[1])
    updatePlotFig(gdpPlot, "GDP", "Year", "Value", gdp[0], gdp[1])
    updatePlotFig(populationPlot, "Population", "Year", "Total Num of Citizens", population[0], population[1])


def updatePlotFig(plot_figure, title, x_label_name, y_label_name, x_values, y_values):
    ax = plot_figure.add_subplot(111)
    ax.set_title(title)
    ax.plot(x_values, y_values)
    ax.set_xlabel(x_label_name)
    ax.set_ylabel(y_label_name)


# initialize UI and global variables
app.startScrollPane("MainWindow", sticky="news")

# frame containing interactive UI elements
app.startFrame("interactive", sticky="news")
app.addLabelOptionBox("Countries", db.getCountryNames(), 0, 0)
app.button("fetch", fetchData, 0, 1)
app.stopFrame()

# frame containing all plots
app.startFrame("Plots", sticky="news")
temperaturePlot = app.addPlotFig("temperature", 0, 0)
emissionPlot = app.addPlotFig("emission", 0, 1)
populationPlot = app.addPlotFig("population", 1, 0)
gdpPlot = app.addPlotFig("gdp", 1, 1)
app.stopFrame()

app.stopScrollPane()

# open UI
app.go()

# close bd connection
db.close()
