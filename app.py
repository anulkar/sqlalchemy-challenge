# Import Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import NumPy and Pandas
import numpy as np
import pandas as pd

# Import Datetime
import datetime as dt

# Import Flask and jsonify
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup: Create the app
app = Flask(__name__)

# ============================================================================================================
# When on the Home page, list all API routes that are available
# ============================================================================================================
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start_date><br>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

# ============================================================================================================
# Define the precipation API route to return all available precipitation scores for Hawaii by date
# ============================================================================================================
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve all the precipitation scores by date
    prcp_scores = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Converts the query results to a Dictionary using date as the key and prcp as the value
    prcp_dict = dict(prcp_scores)

    # Returns the JSON representation of the Dictionary
    return(jsonify(prcp_dict))

# ============================================================================================================
# Define the stations API route to list all Hawaii weather stations from the dataset.
# ============================================================================================================
@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query to return all the station info from the dataset
    stations = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, lat, lng, elev in stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = lat
        station_dict["longitude"] = lng
        station_dict["elevation"] = elev
        all_stations.append(station_dict)

    # Returns the JSON representation of the list
    return(jsonify(all_stations))

# ============================================================================================================
# Define the tobs API route to return dates and temperature observations from a year from the last data point.
# ============================================================================================================
@app.route("/api/v1.0/tobs")
def tobs():

    # Create session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date of the last data point in the database
    last_measurement_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Calculate the date 1 year ago from the last data point in the database
    date_year_ago = dt.datetime.strptime(last_measurement_date[0],'%Y-%m-%d').date() - dt.timedelta(weeks=52)

    # Query for the dates and temperature observations from a year from the last data point
    temp_obs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= date_year_ago).filter(Measurement.date <= last_measurement_date[0]).all()

    session.close()

    # Unpack tuple using list comprehensions
    temps = [temp[1] for temp in temp_obs]

    # Return a JSON list of Temperature Observations (tobs) for the previous year
    return(jsonify(temps))

# ============================================================================================================
# 
# ============================================================================================================
@app.route("/api/v1.0/<start>")
def query_temps_start_date(start_date):

    """ Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date. """
    
    return "TBD"

# ============================================================================================================
# 
# ============================================================================================================
@app.route("/api/v1.0/<start>/<end>")
def query_temps_startend_date(start_date, end_date):

    """ Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive. """
    return "TBD"

if __name__ == "__main__":
    app.run(debug=True)