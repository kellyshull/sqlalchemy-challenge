import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

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
# use &lt; and &gt; as place holders for < > 
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;'>Start Date</a><br/>"
        f"<a href='/api/v1.0/&lt;start&gt;/&lt;end&gt;>End Date</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all results to dictionary using date as key and prcp as value
    prec_query = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()


    session.close()

    # put dict here use {}
    total_prcp = []
    for date, prcp in prec_query:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        total_prcp.append(prcp_dict)

    return jsonify (total_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    station_query = session.query(Station.station, Station.name).all()

    session.close()
    station_list = list(np.ravel(station_query))

    return jsonify(station_list) 





if __name__ == '__main__':
    app.run(debug=True)