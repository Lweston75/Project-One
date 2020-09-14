#%%
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats as st
import numpy as np
from pprint import pprint
import time
#%%

movie_csv = "movies.csv"
movie_df = pd.read_csv(movie_csv, encoding = "ISO-8859-1")

movie_df.head()
# %%
def award_gen(x):
    y = {}
    try:
        x=x.split(" ")
        for i in range(len(x)):
                try:
                    x[i] = int(x[i])
                    y[x[i+1]] = x[i]
                except:
                    pass
        if x[0] == 'Nominated':
            y['nominations.'] += int(x[2])
        return y
    except:
        return "Could not parse awards"

        
movie_df['Awards'] = movie_df['Awards_Blurb'].apply(award_gen)
#%%
# To remove duplicates
movie_df = movie_df.groupby('Const').first()
movie_df.head(20)
#%%
#movie_df.drop('Unnamed:0', axis = 0, inplace = True)
movie_df = movie_df[movie_df['Title Type'] == 'movie']
#for index, row in movie_df.iterrows():


#%%