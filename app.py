import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    print("Server received request for 'Home' page...")
    return (
        f"Add any of the following to the end of the link to see JSON."
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Add date (yyyy-mm-dd) start to see climate data for that date forward. /api/v1.0/<start><br/>"
        f"Add date start (yyyy-mm-dd) and date end (yyyy-mm-dd) to see climate data for that date range. /api/v1.0/<start>/<end>"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()
    session.close()

    precipitation= []

    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp

        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name).\
        order_by(Station.station).all()
    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all temperature data
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station=='USC00519281').\
        order_by(Measurement.date).all()
    session.close()

    tobs = []

    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        tobs.append(tobs_dict)

    return jsonify(stations)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature data after the given start date
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
        
    temp_start = []

    for min, avg, max in results:
        temp_start_dict = {}
        temp_start_dict["Date"] = date
        temp_start_dict["TMIN"] = min
        temp_start_dict["TAVG"] = avg
        temp_start_dict["TMAX"] = max

        temp_start.append(temp_start_dict)

    return jsonify(temp_start)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature data after the given start date and before the given end date
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    start_end_tobs = []

    for date, min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["Date"] = date
        start_end_tobs_dict["TMIN"] = min
        start_end_tobs_dict["TAVG"] = avg
        start_end_tobs_dict["TMAX"] = max

        start_end_tobs.append(start_end_tobs_dict)

    session.close()

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)