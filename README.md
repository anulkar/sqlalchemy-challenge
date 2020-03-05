# Data Science SQL Alchemy Activity: Surfs Up!

## Step 1 - Climate Analysis and Exploration

Used Python and SQLAlchemy to do basic [climate analysis and data exploration](https://github.com/anulkar/sqlalchemy-challenge/blob/master/climate_analysis.ipynb) of the [Hawaii climate database](https://github.com/anulkar/sqlalchemy-challenge/blob/master/Resources/hawaii.sqlite). All of the Precipitation, Temperature and Station analysis was completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

## Step 2 - Climate App

Designed a Flask API based on the queries that were developed as part of Step 1. Used Flask `jsonify` to convert the API data into valid JSON response objects.


### Flask Routes

* `/`
  * Home page that lists all routes that are available.

* `/api/v1.0/precipitation`
  * Returns the JSON representation of the precipitation data dictionary object.

* `/api/v1.0/stations`
  * Returns a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Returns a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  * Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
