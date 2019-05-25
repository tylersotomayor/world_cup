# import necessary libraries
from flask import (
    Flask,
    render_template,
    jsonify,
    request)

from flask_sqlalchemy import SQLAlchemy
import Scrape_WorldCup

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/db.sqlite"

db = SQLAlchemy(app)

class Worldcup18(db.Model):
    __tablename__ = 'WC18'

    teams = db.Column(db.String, primary_key=True)
    matches = db.Column(db.String(64))
    yellow = db.Column(db.integer)
    indirectred = db.Column(db.integer)
    directred = db.Column(db.integer)
    avgfoulscommited = db.Column(db.float)
    avgfoulssuffered = db.Column(db.float)
    penaltiescaused = db.Column(db.integer)

    # def __repr__(self):
    #     return '<Worldcup18 %r>' % (self.nickname)

class Worldcup14(db.Model):
    __tablename__ = 'WC14'

    teams = db.Column(db.String, primary_key=True)
    matches = db.Column(db.String(64))
    yellow = db.Column(db.integer)
    indirectred = db.Column(db.integer)
    directred = db.Column(db.integer)
    avgfoulscommited = db.Column(db.float)
    avgfoulssuffered = db.Column(db.float)
    penaltiescaused = db.Column(db.integer)

    # def __repr__(self):
    #     return '<Worldcup14 %r>' % (self.nickname)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"
    
@app.route("/2018")
def cup2018():
    results = db.session.query(Worldcup18.teams, Worldcup18.matches, Worldcup18.yellow, Worldcup18.indirectred, Worldcup18.directred, Worldcup18.avgfoulscommited, Worldcup18.avgfoulssuffered, Worldcup18.penaltiescaused).all()

    WC18 = []
    for result in results:
        WC18.append({
            "teams": result[0],
            "matches": result[1],
            "yellow": result[2],
            "indirectred": result[3],
            "directred": result[4],
            "avgfoulscommited": result[5],
            "avgfoulssuffered": result[6],
            "penaltiescaused": result[7],
        })
    return jsonify(WC18)

@app.route("/2014")
def cup2014():
    results = db.session.query(Worldcup14.teams, Worldcup14.matches, Worldcup14.yellow, Worldcup14.indirectred, Worldcup14.directred, Worldcup14.avgfoulscommited, Worldcup14.avgfoulssuffered, Worldcup14.penaltiescaused).all()

    WC14 = []
    for result in results:
        WC14.append({
            "teams": result[0],
            "matches": result[1],
            "yellow": result[2],
            "indirectred": result[3],
            "directred": result[4],
            "avgfoulscommited": result[5],
            "avgfoulssuffered": result[6],
            "penaltiescaused": result[7],
        })
    return jsonify(WC14)

if __name__ == "__main__":
    app.run()
