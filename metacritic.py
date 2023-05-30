#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 22:19:20 2023

@author: quentin
"""

#%%
import pandas as pd
import numpy as np
import statistics as st
import matplotlib.pyplot as plt

#%%
meta_genres=pd.read_csv('meta_genres.csv',index_col='Index')
meta_genres=meta_genres[(meta_genres['Metascore'] != 'tbd') & (meta_genres['User Score'] != 'tbd')]
meta_genres=meta_genres[(meta_genres['Metascore'] != 'Error') & (meta_genres['User Score'] != 'Error')]
meta_genres=meta_genres.reset_index(drop=True)

meta_genres=meta_genres.astype({'User Score': float, 'Metascore': int})
meta_genres['User Score'] = meta_genres['User Score'].apply(lambda x : int(x*10))

#%%
## Compare boxplots of players and press.
metascores=meta_genres['Metascore'].to_numpy(dtype=int)
meta_mean=metascores.mean()
meta_median=st.median(metascores.tolist())

userscores=meta_genres['User Score'].to_numpy(dtype=int)
user_mean=userscores.mean()
user_median=st.median(userscores.tolist())

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.tight_layout(pad=2)
fig.set_dpi(300)
ax1.boxplot(metascores, vert=0)
ax1.vlines(meta_mean,0.5,1.5,linestyles="dashed",label="moyenne")
ax1.vlines(meta_median,0.5,1.5,linestyles="dotted",label="médiane")
ax1.legend(shadow=True, fancybox=True,loc="upper left")
ax1.set_title('Boxplot des notes données par la presse (Metacritic, sur 100)')
ax2.boxplot(userscores, vert=0)
ax2.vlines(user_mean,0.5,1.5,linestyles="dashed",label="moyenne")
ax2.vlines(user_median,0.5,1.5,linestyles="dotted",label="médiane")
ax2.legend(shadow=True, fancybox=True,loc="upper left")
ax2.set_title('Boxplot des notes données par les joueurs (Metacritic, sur 100)')

ax1.plot()
ax2.plot()
ax1.set_xlim(xmin=10, xmax=100)
ax2.set_xlim(xmin=10, xmax=100)
plt.show(fig)

#%%
## Get number of games by genre, for the top 5%.
q95=np.quantile(metascores,0.95, method = "inverted_cdf")
meta95=meta_genres[meta_genres['Metascore'] >= q95]

genres95={}
meta95=meta95.reset_index(drop=True)

for i in range(meta95.shape[0]):
    gamegenres=meta95.loc[i,'Genres']
    gamegenres=gamegenres.split(',')
    gamegenres=list(set(gamegenres))
    gamegenres=[genre.strip() for genre in gamegenres]
    
    if 'General' in gamegenres:
        gamegenres.remove('General')
    
    if 'Action Adventure' in gamegenres:
        for genre in ['Action', 'Adventure']:
            if genre in gamegenres:
                gamegenres.remove(genre)

    for genre in gamegenres:
        if genre not in genres95:
            genres95[genre]=1
        else:
            genres95[genre]+=1

genres95_it=genres95.copy()
for genre in genres95:
    if genres95[genre] <= 10:
        del genres95_it[genre]
genres95=genres95_it

genres95=dict(sorted(genres95.items()))

display(genres95)
labels=[]
numbers=[]
for key in genres95:
    labels.append(key)
    numbers.append(genres95[key])

plt.figure(dpi=300)
plt.bar(labels,numbers)
plt.yticks(np.arange(0, 90, 10))
plt.xticks(rotation=45, ha="right")
plt.title('Nombre de jeux par genre (top 5% Metacritic, '+str(meta95.shape[0])+' jeux)')
plt.show()
