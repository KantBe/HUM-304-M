#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 15:36:58 2023

@author: quentin
"""
#%%
import pandas as pd
import numpy as np
import statistics as st
import matplotlib.pyplot as plt

#%%
presse_csv=pd.read_csv('presse.csv')
presse=presse_csv.loc[presse_csv['reviewed_score'].str.isdigit()]
presse=presse.astype({'reviewed_score': float})
presse.loc[27696,'reviewed_score']=presse.loc[27696,'reviewed_score']/2 # Fix score error.
presse=presse.reset_index(drop=True)

## Liste les non digits
#liste=presse.loc[~presse['reviewed_score'].str.isdigit(), 'reviewed_score'].tolist()
#print(liste)

#%%
## Double scores of Gamekult and Canard PC.
i=0
while i < presse.shape[0]:
    score=presse.loc[i,'reviewed_score']
    if presse.loc[i,'source_name'] == 'Gamekult' or presse.loc[i,'source_name'] == 'Canard PC':
        presse.loc[i,'reviewed_score']=2*score
    i+=1

#%%
## Get quartiles and plot boxplot.
scores=presse['reviewed_score'].to_numpy()
mean=scores.mean()
median=st.median(scores.tolist())
q05=np.quantile(scores,0.005, method = "inverted_cdf")
q995=np.quantile(scores,0.995, method = "inverted_cdf")

presse5=presse[presse['reviewed_score'] <= q05]
presse95=presse[presse['reviewed_score'] >= q995]

presse5.to_csv('presse05.csv',index=False)
presse95.to_csv('presse995.csv',index=False)

plt.figure(dpi=300)
plt.boxplot(scores, vert=0)
plt.xticks(np.arange(0, 24, 2))
plt.vlines(mean,0.5,1.5,linestyles="dashed",label="moyenne")
plt.vlines(median,0.5,1.5,linestyles="dotted",label="médiane")
plt.legend(shadow=True, fancybox=True,loc="upper left")
plt.title('Boxplot des notes données par la presse française (sur 20)')
plt.show()

#%%
## Get 5% games around mean.
sorted_presse=presse.sort_values('reviewed_score')
sorted_presse=sorted_presse.reset_index(drop=True)

bot_i=0
top_i=presse.shape[0]
def find_mean_index():
    global bot_i, top_i
    i=int((top_i+bot_i)/2)
    found_score=sorted_presse.loc[i,'reviewed_score']
    if found_score >= mean:
        top_i=i
    else:
        bot_i=i   
    if top_i-bot_i > 1: 
        find_mean_index()    
    
find_mean_index()
mean_index=top_i
percentile_range=int(presse.shape[0]*25/10000)
bot_i=mean_index-percentile_range
top_i=mean_index+percentile_range
bot_score=sorted_presse.loc[bot_i,'reviewed_score']
#top_score=sorted_presse.loc[top_i,'reviewed_score']
top_score=bot_score

sorted_presse=sorted_presse[(sorted_presse['reviewed_score'] >= bot_score) & (sorted_presse['reviewed_score'] <= top_score)]
sorted_presse.to_csv('presse_mean_0,5%.csv',index=False)