# import necessary libraries
#from models import create_classes
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite" #"postgresql://postgres:postgres@localhost:5432/firedata_db"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Fires = Base.classes.fires


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/fires")
def fires():
# Create our session (link) from Python to the DB
    #session = Session(engine)
    
    # Query all fire data
    results = db.session.query(Fires.title, Fires.published, Fires.lat, Fires.lon,
                            Fires.link_url, Fires.description, Fires.cause, Fires.acres).all()

    #session.close()
    
    fire_data = []
    for result in results:
        fire_data.append({
            "title":result[0],
            "published":result[1],
            "lat":result[2],
            "lon":result[3],
            "link_url":result[4],
            "description":result[5],
            "cause":result[6],
            "acres":result[7]})

    return jsonify(fire_data)
    

if __name__ == "__main__":
    app.run()