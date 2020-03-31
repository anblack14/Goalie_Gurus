# Dependencies
import time
import pandas as pd

from sqlalchemy import create_engine

import pymysql
pymysql.install_as_MySQLdb()

# Config Variables 
from config import remote_db_endpoint, remote_db_port
from config import remote_gwsis_dbname, remote_gwsis_dbuser, remote_gwsis_dbpwd

def hrscrape():
    # Cloud MySQl database connection on AWS
    engine = create_engine(f"mysql://{remote_gwsis_dbuser}:{remote_gwsis_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_gwsis_dbname}")

    #Creates current season & gets current season hockey reference data
    currseason = 2020
    seasonname = f'{currseason - 1}-{currseason}'
    url= f'https://www.hockey-reference.com/leagues/NHL_{currseason}_skaters.html'
    currdata = pd.read_html(url,header=1)
    time.sleep(5)
    currdf = currdata[0]

    #drops duplicates for players that were traded
    currdf = currdf.drop_duplicates('Player', keep="first")

    #drop a random ranking row
    droprow = currdf[currdf['Rk'] == "Rk" ].index
    currdf.drop(droprow , inplace=True)

    #creates season column
    currdf['Season']=seasonname

    #casts column types & drops Rk column
    currdf["G"] = currdf["G"].astype(int)
    currdf["GP"] = currdf["GP"].astype(int)
    currdf = currdf.drop(['Rk'], axis=1)

    #rename columns
    currdf = currdf.rename(columns={"Tm": "Team", "G": "Goals_Scored","PS":"Point_Shares","SH":"SHG","GW":"GWG","EV.1":"EV_Assists","PP.1":"PP_Assists","SH.1":"SH_Assists"})

    #create connection to MySQL db
    conn = engine.connect()

    #creates current season hr data table
    currdf.to_sql(name='hr_current_data', if_exists='replace', con=conn, chunksize=500, index=False)        

    #reads historical data table & then combine historical and current data
    df_hist = pd.read_sql('SELECT * FROM hr_hist_data', con=engine)

    df_combine = pd.concat([currdf, df_hist])

    #creates season id & Rk columns
    df_combine.sort_values(['Season','Goals_Scored'], ascending=[True, False], inplace=True)
    df_combine.reset_index(inplace=True, drop=True)
    df_combine['seasonid'] = df_combine.groupby('Player').cumcount() + 1   
    df_combine['Rk'] = df_combine.groupby('Season').cumcount() + 1 

    #create final table
    df_combine.to_sql(name='hr_data', if_exists='replace', con=conn, chunksize=500, index=False)   

    conn.close()

    print("---SCRAPE COMPLETE---")

    return()

#Set a timer for initial deployment
time.sleep(46920)

# Set timer to run every 24 hours...timer is in seconds

# counter just to count how many days it's been running
counter = 0

# Infinite loop
while(True):

    # Call scrape function
    hrscrape()

    # 24 hour sleep timer
    time.sleep(86400)

    # Add 1 to the counter prior to re-running the loop
    counter += 1

    print(counter)
