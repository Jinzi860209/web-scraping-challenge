# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# create instance of Flask app
app = Flask(__name__)

# create mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Flask Routes
@app.route("/")
def home(): 

    # Find data
    scraped_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=scraped_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    scraped_data = scrape_mars.scrape()


    mongo.db.collection.update({}, scraped_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)

