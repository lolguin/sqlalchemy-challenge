import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create an app
app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1).scalar()

    #convert string to date format
    #last_date = datetime.strptime(last_date, '%Y-%m-%d')

    #calculate the previous year from last date
    previous_year = '2016-08-23'

    #query date based on previous year's date
    precip = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= previous_year).\
                order_by(Measurement.date.asc()).all()

    session.close()

    precip_list = list(np.ravel(precip))
    return jsonify(precip_list)

#Define static routes
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"<br/>Available Routes:<br/>"
        f"<br/>/api/v1.0/precipitation<br/>"
        f"/api/v.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)