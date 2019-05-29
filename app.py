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


################################################
# Testing SQLITE creation of tables and adding data
################################################

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO teams_2018(country,played,comitted_f,suffered_f,avg_comitted,avg_suffered,yellow_cards,direct_red_cards,indirect_red_cards)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def trial():
    database = "/Users/kennethgonzalez/Documents/Final_Effort/db/test.sqlite"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)
    if conn is not None:

        # cur = conn.cursor()
        # dropTableStatement = "DROP TABLE projects"
        # dropTableStatement2 = "DROP TABLE tasks"
        # cur.execute(dropTableStatement)
        


        # create projects table
        # create_table(conn, sql_create_projects_table)
        # create tasks table
        # create_table(conn, sql_create_tasks_table)

        with conn:
            # create a new project
            project = ( 'Canada', '7', '11', '32', '4', '3', '43', '23', '12')
            create_project(conn, project)
            # project = ('TESTING', 'TESTING', 'TESING')
            # project_id = create_project(conn, project)

        conn.close()
    else:
        print("Error! cannot create the database connection.")
    

# trial()



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
Samples_Metadata = Base.classes.teams_2018_fixed
Teams_2014 = Base.classes.teams_2014_fixed

#################################################
# Convert SQLITE to CSV
#################################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db/test.sqlite")

conn = sqlite3.connect(db_path)
cur = conn.cursor()
# cur.execute("select * from teams_2018;")

df = pd.read_sql_query("select * from teams_2018_fixed;", conn)
export_csv = df.to_csv (r'/Users/kennethgonzalez/Documents/Final_Effort/db/data.csv', index = None, header=True)
df1 = pd.read_sql_query("select * from teams_2014_fixed;", conn)
export_csv = df1.to_csv (r'/Users/kennethgonzalez/Documents/Final_Effort/db/data1.csv', index = None, header=True)


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

    # renders index.html file and sends the data from csv file
    """Return the homepage."""
    return render_template("index.html", data = data)


@app.route("/index2.html")
def index2():
    
    # Read CSV
    df = pd.read_csv('db/data1.csv')

    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    
    data = {'chart_data': chart_data}

    # renders index.html file and sends the data from csv file
    """Return the homepage."""
    return render_template("index2.html", data = data)


@app.route("/index.html")
def index1():
    
    # Read CSV
    df = pd.read_csv('db/data.csv')

    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    
    data = {'chart_data': chart_data}

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
        # print(json.dumps(list(i.values())))
        t = json.dumps(list(i.values()))

    names = t
    return(names)

#################################################
# Pulls the team names and places them in the dropdown
#################################################

@app.route("/index2.html/names2")
def names2():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Teams_2014.country).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    names = list()
    
    # New code
    for i in df.to_dict().values():
        print(json.dumps(list(i.values())))
        t = json.dumps(list(i.values()))

    names = t
    # print(names)
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
        Samples_Metadata.fouls_committed,
        Samples_Metadata.fouls_suffered,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.country == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["Games Played"] = result[0]
        sample_metadata["Fouls Committed"] = result[1]
        sample_metadata["Fouls Suffered"] = result[2]

    # print(sample_metadata)
    return jsonify(sample_metadata)

@app.route("/index2.html/metadata/<sample>")
def sample_metadata2(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Teams_2014.played,
        Teams_2014.fouls_committed,
        Teams_2014.fouls_suffered,
    ]

    results = db.session.query(*sel).filter(Teams_2014.country == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["Games Played"] = result[0]
        sample_metadata["Fouls Committed"] = result[1]
        sample_metadata["Fouls Suffered"] = result[2]

    # print(sample_metadata)
    return jsonify(sample_metadata)

#################################################
# Stores data in a dictionary so that pie chart can be created
#################################################

@app.route("/samples/<sample>")
def samples(sample):
    sel = [
        Samples_Metadata.played,
        Samples_Metadata.fouls_committed,
        Samples_Metadata.yellow_cards,
        Samples_Metadata.direct_red_cards,
        Samples_Metadata.indirect_red_cards,
        Samples_Metadata.fouls_suffered,
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
        

    # print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/index2.html/samples/<sample>")
def samples2(sample):
    sel = [
        Teams_2014.played,
        Teams_2014.fouls_committed,
        Teams_2014.yellow_cards,
        Teams_2014.red_cards,
        Teams_2014.indirect_red_cards,
        Teams_2014.fouls_suffered,
    ]

    results = db.session.query(*sel).filter(Teams_2014.country == sample).all()

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
        

    # print(sample_metadata)
    return jsonify(sample_metadata)
#################################################
# Stores data for scatter plots
#################################################

# @app.route("/scatter")
# def sample_scatter():
#     # stmt = db.session.query(Samples_Metadata).statement
#     df = pd.read_csv('db/data.csv')

#     data = {
#         "country": df.country.values.tolist(),
#         "comitted_f": df.comitted_f.values.tolist(),
#         "played": df.played.values.tolist(),
#         "suffered_f": df.suffered_f.values.tolist(),
#     }

#     # print(df['country'])
#     return(jsonify(data))
   


if __name__ == "__main__":
    app.run(debug=True)