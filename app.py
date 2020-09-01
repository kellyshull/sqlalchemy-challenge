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
        f"<a href='/api/v1.0/start'>Start Date</a><br/>"
        f"<a href='/api/v1.0/start/end'>End Date</a><br/>"
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

@app.route("/api/v1.0/start")
def start():
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    
    start_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= query_date).all()

    session.close() 

    start_list = list(np.ravel(start_query))


    # start_list = [] ...do not use
    # start_dict = {}
    # for min, avg, maxim in start_query:
    #     start_dict["min"] = min
    #     start_dict["avg"] = avg
    #     start_dict["max"] = max
    
    return jsonify(start_list) 

@app.route("/api/v1.0/start/end")
def end():
    session = Session(engine)

    start_date = dt.date(2016, 8, 23)
    end_date = dt.date(2016, 8, 28)


    end_query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


    session.close() 

    end_list = list(np.ravel(end_query))

    return jsonify(end_list)



if __name__ == '__main__':
    app.run(debug=True)