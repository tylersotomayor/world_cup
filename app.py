import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import json
import sqlite3
import os.path

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/test.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.teams_2018


#################################################
# Convert SQLITE to CSV
#################################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db/test.sqlite")

conn = sqlite3.connect(db_path)
cur = conn.cursor()
# cur.execute("select * from teams_2018;")

df = pd.read_sql_query("select * from teams_2018;", conn)
export_csv = df.to_csv (r'/Users/kennethgonzalez/Documents/Final_Effort/db/data.csv', index = None, header=True)

##################################################
# Beginnning of flask application
#################################################

@app.route("/")
def index():
    
    # Read CSV
    df = pd.read_csv('db/data.csv')

    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    
    data = {'chart_data': chart_data}

    print(data)

    # renders index.html file and sends the data from csv file
    """Return the homepage."""
    return render_template("index.html", data = data)


#################################################
# Pulls the team names and places them in the dropdown
#################################################

@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Samples_Metadata.country).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    names = list()
    
    # New code
    for i in df.to_dict().values():
        print(json.dumps(list(i.values())))
        t = json.dumps(list(i.values()))

    names = t
    return(names)

#################################################
# Pulls the metadata about how many games were played,
# how many fouls were committed, and how many fouls were suffered
#################################################

@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.played,
        Samples_Metadata.comitted_f,
        Samples_Metadata.suffered_f,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.country == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["played"] = result[0]
        sample_metadata["comitted_f"] = result[1]
        sample_metadata["suffered_f"] = result[2]

    print(sample_metadata)
    return jsonify(sample_metadata)

#################################################
# Stores data in a dictionary so that pie chart can be created
#################################################

@app.route("/samples/<sample>")
def samples(sample):
    sel = [
        Samples_Metadata.played,
        Samples_Metadata.comitted_f,
        Samples_Metadata.yellow_cards,
        Samples_Metadata.direct_red_cards,
        Samples_Metadata.indirect_red_cards,
        Samples_Metadata.suffered_f,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.country == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["played"] = result[0]
        sample_metadata["comitted_f"] = result[1]
        sample_metadata["yellow_cards"] = result[2]
        sample_metadata["direct_red_cards"] = result[3]
        sample_metadata["indirect_red_cards"] = result[4]
        sample_metadata["suffered_f"] = result[5]
        sample_metadata["no_action"] = result[1] - result[2] - result[3] - result[4]
        

    print(sample_metadata)
    return jsonify(sample_metadata)

#################################################
# Stores data for scatter plots
#################################################

@app.route("/scatter")
def sample_scatter():
    # stmt = db.session.query(Samples_Metadata).statement
    df = pd.read_csv('db/data.csv')

    data = {
        "country": df.country.values.tolist(),
        "comitted_f": df.comitted_f.values.tolist(),
        "played": df.played.values.tolist(),
        "suffered_f": df.suffered_f.values.tolist(),
    }

    # print(df['country'])
    return(jsonify(data))
   


if __name__ == "__main__":
    app.run(debug=True)