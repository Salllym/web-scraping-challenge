#################################################
# MongoDB and Flask Application
#################################################

# Dependencies and Setup
from flask import Flask, render_template, redirect 
import pymongo 
import scrape_mars
from flask_pymongo import PyMongo

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# PyMongo Connection Setup
#################################################
mongo = PyMongo(app=app,uri = "mongodb://localhost:27017/mars_app")
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)
#################################################
# Flask Routes
#################################################
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    #return "Scraping Successful"
    return redirect("/")

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)