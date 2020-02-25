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
        f"Available API Routes:<br/>"
        f"<a href='http://localhost:5000/api/v1.0/precipitation' target='_blank'>Precipitation API</a><br/>"
        f"<a href='http://localhost:5000/api/v1.0/stations' target='_blank'>Stations API</a><br>"
        f"<a href='http://localhost:5000/api/v1.0/tobs' target='_blank'>Temperature Observations API</a><br>"
        f"TMIN, TAVG, TMAX based on Start Date only: http://localhost:5000/api/v1.0/<start_date><br>"
        f"TMIN, TAVG, TMAX based on Start & End Date: http://localhost:5000/api/v1.0/<start_date>/<end_date>"
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
# Define API route to return TMIN, TAVG, and TMAX for a given start date range
# ============================================================================================================
@app.route("/api/v1.0/<start>")
def query_temps_start_date(start):
    """ 
    Args:
        start_date (string): A date string in the format %Y-%m-%d        
    Returns:
        TMIN, TAVG, and TMAX
    """
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    # Design query to get the minimum temperature, average temperature, and the max temperature for a given start date range.
    # Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
    return(jsonify(temps))

# ============================================================================================================
# Define API route to return TMIN, TAVG, and TMAX for a given start and end date range
# ============================================================================================================
@app.route("/api/v1.0/<start>/<end>")
def query_temps_startend_date(start, end):
    """ 
    Args:
        start (string): A date string in the format %Y-%m-%d        
        end (string): A date string in the format %Y-%m-%d
    Returns:
        TMIN, TAVG, and TMAX
    """
    # Create session (link) from Python to the DB
    session = Session(engine)
    
    # Design query to get the minimum temperature, average temperature, and the max temperature for a given start and end date range.
    # Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start and end date.
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
    return(jsonify(temps))

if __name__ == "__main__":
    app.run(debug=True)