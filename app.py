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
        f"<a href='/api/v1.0/&lt;start&gt;/&lt;end&gt;'>End Date</a><br/>"
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

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    # query the dates and temps of the most active station for the last year of data (copy paste from workbook)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    top_station_query = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= query_date).\
            filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    top_station = []
    for date, tobs in top_station_query:
        top_dict = {}
        top_dict["date"] = date
        top_dict["tobs"] = tobs
        top_station.append(top_dict)
    
    return jsonify(top_station)

@app.route("/api/v1.0/start/&lt;start&gt;")
def start():
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start_query = session.query(*sel).filter(Measurement.date >= query_date).all()

    session.close() 

    # start_list = [] ...do not use
    start_dict = {}
    for mini, avg, maxim in start_query:
        start_dict["min"] = mini
        start_dict["avg"] = avg
        start_dict["max"] = maxim 
    
    return jsonify(start_dict) 


     





if __name__ == '__main__':
    app.run(debug=False)