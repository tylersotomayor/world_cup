from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_WorldCup

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/WorldCup_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    WC = mongo.db.WC.find_one()
    return render_template("index.html", WC=WC)

@app.route("/scrape18")
def scrape():
    WC = mongo.db.WC
    WC_data = scrape_WorldCup.scrape_WC18()
    WC.update({}, WC_data, upsert=True)
    return "Scraping Successful!"

@app.route("/scrape18")
def scrape():
    WC = mongo.db.WC
    WC_data = scrape_WorldCup.scrape_WC14()
    WC.update({}, WC_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()
