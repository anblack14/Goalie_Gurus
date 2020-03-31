import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import os
from datetime import date

from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

# Config Variables 
from config import remote_db_endpoint, remote_db_port
from config import remote_gwsis_dbname, remote_gwsis_dbuser, remote_gwsis_dbpwd

def ov():
    #gets the first model dataframe ready
    engine = create_engine(f"mysql://{remote_gwsis_dbuser}:{remote_gwsis_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_gwsis_dbname}")
    conn = engine.connect()

    df = pd.read_sql('SELECT * FROM top56_scorers_GL_data', con=engine)
    shotpred = pd.read_sql('SELECT * FROM shotpred', con=engine)

    df["shots"] = df["shots"].apply(pd.to_numeric)
    df['sumshots'] = df.groupby('id')['shots'].transform(pd.Series.cumsum)
    df = df.fillna(0)
    df["sumshots"] = df["sumshots"].apply(pd.to_numeric).astype(int)

    skinnydf = df.drop(["games","goals","firstname","lastname","pos","birthdate","team","opp", "date","home","win","assists","ppg","ppp","gwg","otg","shg","shp","pm","pts", "shots", "season","seasonid"], axis=1)

    ovdf = skinnydf.loc[(skinnydf['id'] == 8471214)]

    #createst the first model
    # Assign X (data) and y (target)
    X_shots = ovdf.drop(["sumshots","pim", "hits","bs","sumgoals","id"],axis=1)
    y_shots = ovdf["sumshots"]


    from sklearn.model_selection import train_test_split

    X_train_shots, X_test_shots, y_train_shots, y_test_shots = train_test_split(X_shots, y_shots, train_size=.8, random_state=1)

    from sklearn.linear_model import LinearRegression
    classifier_shots = LinearRegression()

    classifier_shots.fit(X_train_shots, y_train_shots)

    predictions_shots = classifier_shots.predict(X_test_shots)

    predictions_shots_df = pd.DataFrame({"DaysAlive": X_test_shots["daysalive"],"GameID": X_test_shots["gameid"],"Prediction": predictions_shots, "Actual": y_test_shots, "Diff":predictions_shots - y_test_shots}).reset_index(drop=True)
    predictions_shots_df = predictions_shots_df.round(decimals=0).astype(int)

    shotpredictions = classifier_shots.predict(shotpred)

    shotpredictions_df = pd.DataFrame({"daysalive": shotpred["daysalive"],"gameid": shotpred["gameid"],"sumshots": shotpredictions}).reset_index(drop=True)
    shotpredictions_df = shotpredictions_df.round(decimals=0).astype(int)

    #creates the second model
    X_goals = ovdf.drop(["pim", "hits","bs","sumgoals","id"],axis=1)
    y_goals = ovdf["sumgoals"]

    X_train_goals, X_test_goals, y_train_goals, y_test_goals = train_test_split(X_goals, y_goals, train_size=.8, random_state=1)

    classifier_goals = LinearRegression()
    classifier_goals

    classifier_goals.fit(X_train_goals, y_train_goals)

    predictions_goals = classifier_goals.predict(X_test_goals)

    predgoals_df = pd.DataFrame({"DaysAlive": X_test_goals["daysalive"],"GameID": X_test_goals["gameid"],"Prediction": predictions_goals, "Actual": y_test_goals, "Diff":predictions_goals - y_test_goals}).reset_index(drop=True)
    predgoals_df = predgoals_df.round(decimals=0).astype(int)

    goalspredictions = classifier_goals.predict(shotpredictions_df)

    goalspredictions_df = pd.DataFrame({"daysalive": shotpredictions_df["daysalive"],"gameid": shotpredictions_df["gameid"], "sumshots":shotpredictions_df["sumshots"], "sumgoals":goalspredictions}).reset_index(drop=True)
    goalspredictions_df = goalspredictions_df.round(decimals=0).astype(int)
    goalspredictions_df = goalspredictions_df.drop(["daysalive","sumshots"], axis=1)
    ovpredictions_df = ovdf.drop(["sumshots","pim", "hits","bs","daysalive","id"],axis=1).reset_index(drop=True)
    goalspredictions_df = pd.concat([ovpredictions_df, goalspredictions_df])

    goalspredictions_df.to_sql(name='ovdb', if_exists='replace', con=conn, chunksize=500, index=False)   


    #creates the predictions table 
    predtable = pd.read_sql('SELECT * FROM predtable', con=engine)
    today = date.today()
    tiegame = goalspredictions_df.loc[goalspredictions_df['sumgoals'] == 894]["gameid"].values[0].astype(int)
    predtable = predtable.append({'Date' : today , 'Game Prediction' : tiegame} , ignore_index=True)
    predtable.to_sql(name='predtable', if_exists='replace', con=conn, chunksize=500, index=False)
    predtable
    predtable_html = predtable.to_html(classes="table table-striped")
    predtable_html = predtable_html.replace('\n', '')

    conn.close()

#Set a timer for initial deployment    
time.sleep(49320)

    # Set timer to run every 24 hours...timer is in seconds

# counter just to count how many days it's been running
counter = 0

# Infinite loop
while(True):

    # Call scrape function
    ov()

    # 24 hour sleep timer
    time.sleep(86400)

    # Add 1 to the counter prior to re-running the loop
    counter += 1

    print(counter)

