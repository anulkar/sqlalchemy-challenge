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

# Create session (link) from Python to the DB
session = Session(engine)

# Flask Setup: Create the app
app = Flask(__name__)

# When on the Home page, list all API routes that are available
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

@app.route("/api/v1.0/precipitation")
def precipitation():
    return "Atul Nulkar: Atlanta, GA"

@app.route("/api/v1.0/stations")
def stations():
    return "Email me at nulkar@gmail.com"

@app.route("/api/v1.0/tobs")
def tobs():
    return "Email me at nulkar@gmail.com"

@app.route("/api/v1.0/<start>")
def query_temps_start_date():
    return "Email me at nulkar@gmail.com"

@app.route("/api/v1.0/<start>/<end>")
def query_temps_startend_date():
    return "Email me at nulkar@gmail.com"

if __name__ == "__main__":
    app.run(debug=True)