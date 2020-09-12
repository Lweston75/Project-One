#%%
import pandas as pd
from matplotlib import pyplot as pyplot
from scipy import stats as st
import numpy as np
from config import key as OMDBkey
from config import bigKey
import requests as req
import json
from pprint import pprint
#key = bigKey
key = OMDBkey
#%%
#Getting the CSV in,  there was a weird encoding error, the ISO-8859 fixes it.
#We'll see if we can change it so that this step is unnecessary when processing
#subsequently published CSVs
movie_csv = "ESP-Movie.csv"
main_df = pd.read_csv(movie_csv, encoding = "ISO-8859-1")
main_df.drop(['Created','Modified','Position','Description','Title Type'],axis=1, inplace = True)


#%%

ID = 'tt1872181'
call = f"http://www.omdbapi.com/?i={ID}&apikey={key}"
data = req.get(call).json()
pprint(data)

#%%
main_df['Box_Office']=''
main_df['Rotten_Tomatoes_Rating']=''
main_df['Metacritic_Rating']=''
main_df['Rated']= ''
main_df['Oscars']= ''
main_df['Total_Awards']= ''
main_df['Total_Nominations'] = ''
main_df['Home_Release']=''
main_df['Production']=''
main_df['Country']=''

# vvv Comment out below when the code is all ready to go vvv
main_df=main_df.head()
# ^^^                                                        ^^^

#This busy monstrosity below is to pull the data we need from OMDB
#We are very limited as to how many calls we can make in a day so we needed
#   to get it all in one 'for' block
for index, row in main_df.iterrows():
    ID = row['Const']
    call = f"http://www.omdbapi.com/?i={ID}&apikey={OMDBkey}"
    data = req.get(call).json()
    main_df.loc[index,'Box_Office'] = data['BoxOffice']
    main_df.loc[index, 'Rated'] = data['Rated']
    main_df.loc[index, 'Production'] = data['Production']
    main_df.loc[index, 'Country'] = data['Country']
#There are many different formats for the sentence which can extract awards information
#The following monstrosity of nested Try blocks in an attempt to get what we need anyway.
#A regex pattern identifier might be a better way but I don't know how to do that yet.
    awards_sent = data['Awards'].split(' ')
    try:
        main_df.loc[index, 'Oscars'] = int(awards_sent[1])
        main_df.loc[index, 'Total_Awards'] = int(awards_sent[4] + row['Oscars'])
        main_df.loc[index, 'Total_Nominations'] = int(awards_sent[-2])
    except:
        try:
            main_df.loc[index, 'Oscars'] = 0
            main_df.loc[index, 'Total_Awards'] = int(awards_sent[5])
            main_df.loc[index, 'Total_Nominations'] = int(awards_sent[-2] + awards_sent[2])
        except:
            try:
                main_df.loc[index, 'Oscars'] = 0
                main_df.loc[index, 'Total_Awards'] = int(awards_sent[0])
                main_df.loc[index, 'Total_Nominations'] = int(awards_sent[-2])
            except:
                main_df.loc[index, 'Oscars'] = np.NaN
                main_df.loc[index, 'Total_Awards'] = np.NaN
                main_df.loc[index, 'Total_Nominations'] = np.NaN
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
    
#%%
#The following functions are to be applied to cells to clean them up

#This cleans up cells tarting with a '$' and handles numbers with commas
def dollarCleaner(x):
    x = x.replace('$','')
    x = x.replace(',','')
    try:
        x = int(x)
    except:
        x = np.NaN
    return x

#This one is made for Rotten Tomatoes ratings, but will remove the percent sign from
#any number
def lessRottenTomato(x):
    x = x.replace('%','')
    try:
        x = int(x)
    except:
        x = np.NaN
    return x

# This one is designed for metacritic and will take the top number from top/bottom format
def megacritic(x):
    x = x.split('/')
    x = x[0]
    try:
        x = int(x)
    except:
        x = np.NaN
    return x

#This will extract the numerical month as long as it is the center value in 
#a string separated by '-'
def monthGetter(x):
    x = x.split('-')
    x = x[1]
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
def dateFormatter(x):
    x = x.split(' ')
    y = f"{x[2]}-{x[1]}-{x[0]}"
    return y
main_df['Box_Office'] = main_df['Box_Office'].apply(dollarCleaner)
main_df['Rotten_Tomatoes_Rating'] = main_df['Rotten_Tomatoes_Rating'].apply(lessRottenTomato)
main_df['Metacritic_Rating'] = main_df['Metacritic_Rating'].apply(megacritic)
main_df['Month Released'] = main_df['Release Date'].apply(monthGetter)
main_df['Genres']= main_df['Genres'].apply(genreSplitter)
main_df['Home_Release']= main_df['Home_Release'].apply(dateFormatter)
# %%
main_df
# %%
