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
main_df.head()

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
small_df=main_df.head()
for index, row in small_df.iterrows():
    ID = row['Const']
    call = f"http://www.omdbapi.com/?i={ID}&apikey={OMDBkey}"
    data = req.get(call).json()
    small_df.at[index,'Box_Office'] = data['BoxOffice']
    if len(data['Ratings'])>0:
        for i in data['Ratings']:
            if i['Source'] == 'Rotten Tomatoes':
                small_df.at[index,'Rotten_Tomatoes_Rating'] = i['Value']
            if i['Source'] == 'Metacritic':
                small_df.at[index,'Metacritic_Rating'] = i['Value']

small_df
# %%
