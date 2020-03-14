# Dependencies
import time
import pandas as pd
import requests
import json
import numpy as np
from datetime import date, datetime

from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

# Config Variables 
from config import remote_db_endpoint, remote_db_port
from config import remote_gwsis_dbname, remote_gwsis_dbuser, remote_gwsis_dbpwd

def currseasonscorersscrape():
    # Cloud MySQl database connection on AWS
    engine = create_engine(f"mysql://{remote_gwsis_dbuser}:{remote_gwsis_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_gwsis_dbname}")

    #Get top 20 active scorers from hockey reference:
    currseason = 2020
    seasonname = f'{currseason - 1}-{currseason}'
    url= f'https://www.hockey-reference.com/leaders/goals_active.html'
    currscorers = pd.read_html(url,header=1)
    time.sleep(5)
    currscorers = currscorers[0]
    currscorers = currscorers.reset_index().T.reset_index().T
    currscorers.reset_index(inplace=True, drop=True)
    currscorers = currscorers[2].head(20)

    currscorerslist = []

    for scorers in currscorers:
        currscorerslist.append(scorers)
        
    #Read in PlayerDF database.  This will need to be replaced with reading the playerdf database table into a DF.  This code creates a new column in the playerdf database, so we can look up to it to get player ids.
    playerdf = pd.read_sql('SELECT * FROM player_data', con=engine)
    playerdf["FL"] = playerdf["firstname"] + " " + playerdf["lastname"]

    #This looks at the active scorers names and looks up the newly created FL column in the playerdf in order to get the top 20 active scorers player ids
    scorerid = []
    for player in currscorerslist:
        scorerid.append(playerdf.loc[playerdf['FL'] == player,"id"].iloc[0])

    #creates the gamelog df
    df = pd.DataFrame(columns=['id','firstname','lastname','pos','birthdate','daysalive','season','seasonid','gameid','assists','goals','sumgoals','pim','shots','games','hits','ppg','ppp','gwg','otg','shg','shp','bs','pm','pts','team','opp','date','home','win'])

    #grabs the current season gamelogs for each top 20 active scorer
    #create season paramaters list
    seasonid = 20192020

    for scorer in scorerid:
        
        try:
            #creates api call 
            person_url = f"http://statsapi.web.nhl.com/api/v1/people/{scorer}/"
            person = requests.get(person_url).json()
            
            #tests api to make sure it has data
            person["people"][0]["id"]

            try:
                #test if the player played in this season.  If not, it will produce an error and go to the next season
                gamelog_url = f"http://statsapi.web.nhl.com/api/v1/people/{scorer}/stats/?stats=gameLog&season={seasonid}"
                gamelogs = requests.get(gamelog_url).json()
                gamelogs["stats"][0]["splits"][0]

                #Loop through game logs within the season and grab various stats
                for game in range(len(gamelogs["stats"][0]["splits"])):

                    #Player info
                    df.loc[len(df.index), "id"] = scorer
                    df.loc[len(df.index)-1, "firstname"] = person["people"][0]["firstName"]
                    df.loc[len(df.index)-1, "lastname"] = person["people"][0]["lastName"]
                    df.loc[len(df.index)-1, "birthdate"] = person["people"][0]["birthDate"]
                    df.loc[len(df.index)-1, "pos"] = person["people"][0]['primaryPosition']['code'] 

                    #Calculate days alive based on game date - birhdate
                    origindate = datetime.strptime(df.loc[len(df.index)-1, "birthdate"], '%Y-%m-%d')
                    lastdate = datetime.strptime(gamelogs["stats"][0]["splits"][game]["date"] , '%Y-%m-%d')
                    df.loc[len(df.index)-1, "daysalive"] = (lastdate - origindate).days

                    #adds season & season id
                    df.loc[len(df.index)-1, "season"] = gamelogs["stats"][0]["splits"][0]["season"]
                    df.loc[len(df.index)-1, "seasonid"] = seasonid

                    #Stats pull...API address for stats: gamelogs["stats"][0]["splits"][0]["stat"]
                    try:
                        df.loc[len(df.index)-1, "assists"] = gamelogs["stats"][0]["splits"][game]["stat"]["assists"]
                    except (KeyError, IndexError):
                        pass#print("Missing assists field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "goals"] = gamelogs["stats"][0]["splits"][game]["stat"]["goals"]
                    except (KeyError, IndexError):
                        pass#print("Missing goals field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "pim"] = gamelogs["stats"][0]["splits"][game]["stat"]["pim"]
                    except (KeyError, IndexError):
                        pass#print("Missing pim field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "shots"] = gamelogs["stats"][0]["splits"][game]["stat"]["shots"]
                    except (KeyError, IndexError):
                        pass#print("Missing shots field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "games"] = gamelogs["stats"][0]["splits"][game]["stat"]["games"]
                    except (KeyError, IndexError):
                        pass#print("Missing games field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "hits"] = gamelogs["stats"][0]["splits"][game]["stat"]["hits"]
                    except (KeyError, IndexError):
                        pass#print("Missing hits field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "ppg"] = gamelogs["stats"][0]["splits"][game]["stat"]["powerPlayGoals"]
                    except (KeyError, IndexError):
                        pass#print("Missing ppg field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "ppp"] = gamelogs["stats"][0]["splits"][game]["stat"]["powerPlayPoints"]
                    except (KeyError, IndexError):
                        pass#print("Missing ppp field/result... skipping.")     
                    try:
                        df.loc[len(df.index)-1, "gwg"] = gamelogs["stats"][0]["splits"][game]["stat"]["gameWinningGoals"]
                    except (KeyError, IndexError):
                        pass#print("Missing gwg field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "otg"] = gamelogs["stats"][0]["splits"][game]["stat"]["overTimeGoals"]
                    except (KeyError, IndexError):
                        pass#print("Missing otg field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "shg"] = gamelogs["stats"][0]["splits"][game]["stat"]["shortHandedGoals"]
                    except (KeyError, IndexError):
                        pass#print("Missing shg field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "shp"] = gamelogs["stats"][0]["splits"][game]["stat"]["shortHandedPoints"]
                    except (KeyError, IndexError):
                        pass#print("Missing shp field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "bs"] = gamelogs["stats"][0]["splits"][game]["stat"]["blocked"]
                    except (KeyError, IndexError):
                        pass#print("Missing bs field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "pm"] = gamelogs["stats"][0]["splits"][game]["stat"]["plusMinus"]
                    except (KeyError, IndexError):
                        pass#print("Missing pm field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "pts"] = gamelogs["stats"][0]["splits"][game]["stat"]["points"]
                    except (KeyError, IndexError):
                        pass#print("Missing pts field/result... skipping.")    

                    #Game info
                    try:
                        df.loc[len(df.index)-1, "team"] = gamelogs["stats"][0]["splits"][game]["team"]["name"]
                    except (KeyError, IndexError):
                        pass#print("Missing team field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "opp"] = gamelogs["stats"][0]["splits"][game]["opponent"]["name"]
                    except (KeyError, IndexError):
                        pass#print("Missing opp field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "date"] = gamelogs["stats"][0]["splits"][game]["date"]
                    except (KeyError, IndexError):
                        pass#print("Missing date field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "home"] = gamelogs["stats"][0]["splits"][game]["isHome"]
                    except (KeyError, IndexError):
                        pass#print("Missing home field/result... skipping.")    
                    try:
                        df.loc[len(df.index)-1, "win"] = gamelogs["stats"][0]["splits"][game]["isWin"]
                    except (KeyError, IndexError):
                        pass#print("Missing win field/result... skipping.")

            #error if the player didn't play in this season
            except (KeyError, IndexError):
                pass#print(f"Missing season {season}... skipping.") 
                    
            print(f"-----Player ID: {scorer} complete-----")
                
        #error if player is missing   
        except (KeyError, IndexError):
                print(f"Missing playerid: {scorer}... skipping.")

    #convert ID to numeric, so we can send data to MySQL
    df["id"] = df["id"].apply(pd.to_numeric)
    
    #create active 20 goal scorers MySQL table
    conn = engine.connect()

    df.to_sql(name='top20_active_GL_current_data', if_exists='replace', con=conn, chunksize=500, index=False)

    #create historical data table & then combine historical and current data
    df_hist = pd.read_sql('SELECT * FROM top20_active_GL_historic_data', con=engine)

    df_combine = pd.concat([df, df_hist])

    #sort by days alive
    df_combine.sort_values(['id','daysalive'], inplace=True)
    df_combine.reset_index(drop=True, inplace=True)

    #calculate cumulative goals & game ID
    df_combine['sumgoals'] = df_combine.groupby('id')['goals'].transform(pd.Series.cumsum)
    df_combine['gameid'] = df_combine.groupby('id').cumcount() + 1   

    #create final table
    df_combine.to_sql(name='top20_active_GL_data', if_exists='replace', con=conn, chunksize=500, index=False)   

    conn.close()

    print("---SCRAPE COMPLETE---")
    return()



#Set a timer for initial deployment    
time.sleep(86400)

    # Set timer to run every 24 hours...timer is in seconds

# counter just to count how many days it's been running
counter = 0

# Infinite loop
while(True):

    # Call scrape function
    currseasonscorersscrape()

    # 24 hour sleep timer
    time.sleep(86400)

    # Add 1 to the counter prior to re-running the loop
    counter += 1

    print(counter)