#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats as st
def Scatter_w_Trend(df,x,y):
    new_df = df[[x,y]].dropna()
    new_df[x] = new_df[x].astype(float)
    new_df[y] = new_df[y].astype(int)
    new_df.head()
    x_list = new_df[x].tolist()
    y_list = new_df[y].tolist()
    plt.scatter(x_list, y_list, alpha = 0.15, color = 'navy')
    m, b, rSquare, pValue, stderr = st.linregress(x_list,y_list)
    line = "y = " + str(round(m,2)) + "x + " + str(round(b,2))
    plt.annotate(line, color="black")
    plt.annotate(f"P = {pValue}",(2,650000000), color = 'black' )
    fit_line_y = new_df[x] * m + b
    plt.plot(x_list, fit_line_y, color = 'black')