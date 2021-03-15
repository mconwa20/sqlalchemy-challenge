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
Station - Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to the Climate API Home page!"
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()

    prcp_date = []

    for date, prcp in results:
        prcp_d_dict = {}
        prcp_d_dict["date"] = date
        prcp_d_dict["prcp"] = prcp

        prcp_date.append(prcp_d_dict)

    session.close()

    return jsonify(prcp_date)

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name).\
        order_by(Station.station).all()

    stations = list(np.ravel(results))

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all temperature data
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.station=='USC00519281').\
        order_by(Measurement.date).all()

    tobs = []

    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        all_tobs.append(tobs_dict)

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature data after the given start date
    results = session.query(Measurement.date,\
        func.min(Measurement.tobs),\
        func.avg(Measurement.tobs),\
        func.max(Measurement.tobs).\
        filter(Measurement.date >= start).all()
        
    start_tobs= []

    for min, avg, max in results:
        start_tobs_dict = {}
        start_tobs_dict["Date"] = date
        start_tobs_dict["TMIN"] = min
        start_tobs_dict["TAVG"] = avg
        start_tobs_dict["TMAX"] = max

        start_tobs.append(start_tobs_dict)

    session.close()

    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temperature data after the given start date and before the given end date
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    start_end_tobs = []

    for prcp, date, tobs in results:
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
