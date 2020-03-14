import pandas as pd

import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import sqlalchemy
from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Heroku check
is_heroku = False
if 'IS_HEROKU' in os.environ:
    is_heroku = True


if is_heroku == False:
    from config import remote_db_endpoint, remote_db_port,remote_gwsis_dbuser, remote_gwsis_dbpwd, remote_db_name
else:
    remote_db_endpoint = os.environ.get('remote_db_endpoint')
    remote_db_port = os.environ.get('remote_db_port')
    remote_gwsis_dbuser = os.environ.get('remote_gwsis_dbuser')
    remote_gwsis_dbpwd = os.environ.get('remote_gwsis_dbpwd')
    remote_db_name = os.environ.get('remote_db_name')


engine = create_engine(
    f"mysql+mysqldb://{remote_gwsis_dbuser}:{remote_gwsis_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")
conn = engine.connect()

# Initialize Flask application
app = Flask(__name__)


# Set up your default route
@app.route('/')
def home():
    return render_template('index.html')

# Set up your default route
@app.route('/api')
def api():
    return render_template('api.html')

# Set up your default route
@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

@app.route('/api/data/current_scorers_data')
def getcurrent_scorers_data():
    # Establish DB connection
    conn = engine.connect()
    try:
        data = pd.read_sql("SELECT * FROM top56_scorers_GL_data ", conn)
        print("Connected")
        return data.to_json(orient='records')
    except Exception as e:
        print(e)
        return render_template('error.html', error=True)


@app.route('/api/data/historic_data')
def gethistoric_data():
    # Establish DB connection
    conn = engine.connect()
    try:
        data = pd.read_sql("SELECT * FROM hr_data ", conn)
        return data.to_json(orient='records')
    except Exception as e:
        print(e)
        return render_template('error.html', error=True)


@app.route('/api/data/ovdb')
def getOVDB():
    # Establish DB connection
    conn = engine.connect()
    try:
        data = pd.read_sql("SELECT * FROM ovdb ", conn)
        return data.to_json(orient='records')
    except Exception as e:
        print(e)
        return render_template('error.html', error=True)


@app.route('/api/data/player_data')
def getplayer_data():
    # Establish DB connection
    conn = engine.connect()
    try:
        data = pd.read_sql("SELECT * FROM player_data ", conn)
        return data.to_json()
    except Exception as e:
        print(e)
        return render_template('error.html', error=True)


@app.route('/api/data/scorers_data')
def getscorers_data():
    # Establish DB connection
    conn = engine.connect()
    try:
        data = pd.read_sql("SELECT * FROM scorers_data ", conn)
        return data.to_json()
    except Exception as e:
        print(e)
        return render_template('error.html', error=True)


@app.route('/api/data/stats_data')
def getstats_data():
    # Establish DB connection
    conn = engine.connect()
    try:
        data = pd.read_sql("SELECT * FROM stats_data ", conn)
        return data.to_json()
    except Exception as e:
        print(e)
        return render_template('error.html', error=True)


if __name__ == "__main__":
    app.run(debug=True)
