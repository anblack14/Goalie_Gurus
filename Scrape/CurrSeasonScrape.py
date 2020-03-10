# Dependencies
import time
import pandas as pd

def currseasonscrape():
    currseason = 2020
    seasonname = f'{currseason - 1}-{currseason}'
    url= f'https://www.hockey-reference.com/leagues/NHL_{currseason}_skaters.html'
    currdata = pd.read_html(url,header=1)
    time.sleep(5)
    currdf = currdata[0]

    currdf = currdf.drop_duplicates('Player', keep="first")

    droprow = currdf[currdf['Rk'] == "Rk" ].index
    currdf.drop(droprow , inplace=True)

    currdf['Season']=seasonname
    currdf['Year']=currseason

    currdf["G"] = currdf["G"].astype(int)
    currdf["GP"] = currdf["GP"].astype(int)
    currdf = currdf.sort_values(["G","GP"], ascending=[False,True])
    currdf.reset_index(inplace=True, drop=True)
    currdf['Rk'] = currdf.index+1

    currdf = currdf.rename(columns={"Tm": "Team", "G": "Goals_Scored","PS":"Point_Shares","SH":"SHG","GW":"GWG","EV.1":"EV_Assists","PP.1":"PP_Assists","SH.1":"SH_Assists"})

    return(currdf)

# Set timer to run every 24 hours...timer is in seconds

# counter just to count how many days it's been running
counter = 0

# Infinite loop
while(True):

    # Call the TweetQuotes function and specify the tweet number
    currseasonscrape()

    # Once tweeted, wait 24 hours before doing anything else
    time.sleep(86400)

    # Add 1 to the counter prior to re-running the loop
    counter += 1
