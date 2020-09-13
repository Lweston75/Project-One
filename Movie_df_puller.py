#%%
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats as st
import numpy as np
from config import key as OMDBkey
from config import bigKey
import requests as req
import json
from pprint import pprint
import time
key = bigKey
#key = OMDBkey
print(bigKey)
#%%
#Getting the CSV in,  there was a weird encoding error, the ISO-8859 fixes it.
#We'll see if we can change it so that this step is unnecessary when processing
#subsequently published CSVs
movie_csv = "ESP-Movie.csv"
main_df = pd.read_csv(movie_csv, encoding = "ISO-8859-1")
main_df.drop(['Created','Modified','Position','Description'],axis=1, inplace = True)


#%%

ID = 'tt0094291'
call = f"http://www.omdbapi.com/?i={ID}&apikey={key}"
data = req.get(call).json()


#%%
main_df['Box_Office']=''
main_df['Rotten_Tomatoes_Rating']=''
main_df['Metacritic_Rating']=''
main_df['Rated']= ''
main_df['Home_Release']=''
main_df['Production']=''
main_df['Country']=''
main_df['Awards_Blurb']=''
main_df['Languages']=''
#%%
# vvv Comment out below when the code is all ready to go vvv
#main_df=main_df.head()
# ^^^                                                        ^^^

#This busy monstrosity below is to pull the data we need from OMDB
#We are very limited as to how many calls we can make in a day so we needed
#   to get it all in one 'for' block
count = 0
for index, row in main_df.iterrows():
    count += 1
    try:
        print(f"#{count}: Getting data for {row['Title']}")
        ID = row['Const']
        call = f"http://www.omdbapi.com/?i={ID}&apikey={key}"
        data = req.get(call).json()
        main_df.loc[index,'Box_Office'] = data['BoxOffice']
        main_df.loc[index, 'Rated'] = data['Rated']
        main_df.loc[index, 'Production'] = data['Production']
        main_df.loc[index, 'Country'] = data['Country']
#Rotten Tomatoes rating information is in a stupid format
#Here is how we had to pull it out:
        if len(data['Ratings'])>0:
            for i in data['Ratings']:
                if i['Source'] == 'Rotten Tomatoes':
                    main_df.loc[index,'Rotten_Tomatoes_Rating'] = i['Value']
                if i['Source'] == 'Metacritic':
                    main_df.loc[index,'Metacritic_Rating'] = i['Value']
        try:
            main_df.loc[index, 'Home_Release'] = data['DVD']
        except:
            main_df.loc[index, 'Home_Release'] = np.NaN
        main_df.loc[index, 'Awards_Blurb'] = data['Awards']
        main_df.loc[index, 'Languages'] = data['Language']
    except:
        print(f"Unable to get data for {row['Title']}")



    
#%%
#The following functions are to be applied to cells to clean them up
#This cleans up cells starting with a '$' and handles numbers with commas
def dollarCleaner(x):
    try:
        x = x.replace('$','')
        x = x.replace(',','')
        x = int(x)
    except:
        x = np.NaN
    return x

#This one is made for Rotten Tomatoes ratings, It removes percent signs from the beginning
def lessRottenTomato(x):
    try:
        x = x.replace('%','')
        x = int(x)
    except:
        x = np.NaN
    return x

# This one is designed for metacritic and will take the top number from "top/bottom" format
def megacritic(x):
    try:
        x = x.split('/')
        x = x[0]
        x = int(x)
    except:
        x = np.NaN
    return x

#This will extract the numerical month as long as it is the center value in 
#a string separated by '-'
def monthGetter(x):
    try:
        x = x.split('-')
        x = x[1]
    except:
        x = np.NaN
    try:
        x = int(x)
    except:
        x = np.NaN
    return x

#This one is designed to split the values in the 'Genres' column into lists
def genreSplitter(x):
    y = []
    try:
        y = x.split(',')
    except:
        y.append(x)
    return y
#This one is to put the date in 'Home Release' into the same fomat as the other dates
#(turning 'May' into '5' will be another story)
def dateFormatter(x):
    y=0
    try:
        x = x.split(' ')
        y = f"{x[2]}-{x[1]}-{x[0]}"
        return y
    except:
        return y
main_df['Box_Office'] = main_df['Box_Office'].apply(dollarCleaner)
main_df['Rotten_Tomatoes_Rating'] = main_df['Rotten_Tomatoes_Rating'].apply(lessRottenTomato)
main_df['Metacritic_Rating'] = main_df['Metacritic_Rating'].apply(megacritic)
main_df['Month Released'] = main_df['Release Date'].apply(monthGetter)
main_df['Genres']= main_df['Genres'].apply(genreSplitter)
main_df['Home_Release']= main_df['Home_Release'].apply(dateFormatter)
main_df['Languages']= main_df['Languages'].apply(genreSplitter)
#%%

main_df.to_csv('movies.csv')
#main_df['Awards_Blurb'].unique()

# %%
main_df.head()

# %%
