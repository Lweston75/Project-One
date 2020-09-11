#%%
import pandas as pd
from matplotlib import pyplot as pyplot
from scipy import stats as st
import numpy as np
from config import key as OMDBkey
import requests as req
import json
from pprint import pprint
#%%
#Getting the CSV in,  there was a weird encoding error, the ISO-8859 fixes it.
#We'll see if we can change it so that this step is unnecessary when processing
#subsequently published CSVs
movie_csv = "ESP-Movie.csv"
main_df = pd.read_csv(movie_csv, encoding = "ISO-8859-1")
main_df.drop(['Created','Modified','Position','Description','Title Type'],axis=1, inplace = True)


#%%

ID = 'tt0110912'
call = f"http://www.omdbapi.com/?i={ID}&apikey={OMDBkey}"
data = req.get(call).json()
print(main_df['Const'].head())
pprint(data['BoxOffice'])
pprint(data['Ratings'][1]['Value'])
#%%
main_df['Box_Office']=''
main_df['Rotten_Tomatoes_Rating']=''
main_df['Metacritic_Rating']=''
main_df=main_df.head()
for index, row in main_df.iterrows():
    ID = row['Const']
    call = f"http://www.omdbapi.com/?i={ID}&apikey={OMDBkey}"
    data = req.get(call).json()
    main_df.loc[index,'Box_Office'] = data['BoxOffice']
    if len(data['Ratings'])>0:
        for i in data['Ratings']:
            if i['Source'] == 'Rotten Tomatoes':
                main_df.loc[index,'Rotten_Tomatoes_Rating'] = i['Value']
            if i['Source'] == 'Metacritic':
                main_df.loc[index,'Metacritic_Rating'] = i['Value']
#%%
def dollarCleaner(x):
    x = x.split('$')
    x = x[-1]
    x = x.replace(',','')
    try:
        x = int(x)
    except:
        x = np.NaN
    return x
def lessRottenTomato(x):
    x = x.split('%')
    x = x[0]
    try:
        x = int(x)
    except:
        x = np.NaN
    return x
def megacritic(x):
    x = x.split('/')
    x = x[0]
    try:
        x = int(x)
    except:
        x = np.NaN
    return x
def monthGetter(x):
    x = x.split('-')
    x = x[1]
    try:
        x = int(x)
    except:
        x = np.NaN
    return x

main_df['Box_Office'] = main_df['Box_Office'].apply(dollarCleaner)
main_df['Rotten_Tomatoes_Rating'] = main_df['Rotten_Tomatoes_Rating'].apply(lessRottenTomato)
main_df['Metacritic_Rating'] = main_df['Metacritic_Rating'].apply(megacritic)
main_df['Month Released'] = main_df['Release Date'].apply(monthGetter)
main_df
# %%
