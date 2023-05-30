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
steam_csv=pd.read_csv('steam.csv')
steam=steam_csv[steam_csv['nb_reviews_total'] >= 1000]
steam=steam.dropna(subset=['store_uscore'])

#%%
## Get 5% worst scores and 95% best scores and plot boxplot.
scores=steam['store_uscore'].to_numpy(dtype=int)
mean=scores.mean()
median=st.median(scores.tolist())
q5=np.quantile(scores,0.05, method = "inverted_cdf")
q95=np.quantile(scores,0.95, method = "inverted_cdf")
print(q5)
print(q95)

steam5=steam[steam['store_uscore'] <= q5]
steam95=steam[steam['store_uscore'] >= q95]

steam5.to_csv('steam5.csv',index=False)
steam95.to_csv('steam95.csv',index=False)

plt.figure(dpi=300)
plt.boxplot(scores, vert=0)
plt.xticks(np.arange(0, 110, 10))
plt.vlines(mean,0.5,1.5,linestyles="dashed",label="moyenne")
plt.vlines(median,0.5,1.5,linestyles="dotted",label="médiane")
plt.legend(shadow=True, fancybox=True,loc="upper left")
plt.title('Boxplot des notes données par les joueurs (Steam, sur 100)')
plt.show()

#%%
## Get scores by genre.
genres={}
steam=steam.reset_index(drop=True)

for i in range(steam.shape[0]):
    score=steam.loc[i,'store_uscore']
    gamegenres=steam.loc[i,'genres']
    gamegenres=gamegenres.split(',')

    for genre in gamegenres:
        if genre not in genres:
            genres[genre]=[]
        genres[genre].append(score)

labels=[]
means=[]
for key in genres:
    labels.append(key)
    means.append(st.mean(genres[key]))

plt.figure(dpi=300)
plt.bar(labels,means)
plt.yticks(np.arange(0, 110, 10))
plt.xticks(rotation=45, ha="right")
plt.title('Moyenne des notes données par genre (Steam, sur 100)')
plt.show()

#%%
## Get 5% games around the mean.
sorted_steam=steam.sort_values('store_uscore')
sorted_steam=sorted_steam.reset_index(drop=True)

bot_i=0
top_i=steam.shape[0]
def find_mean_index():
    global bot_i, top_i
    i=int((top_i+bot_i)/2)
    found_score=sorted_steam.loc[i,'store_uscore']
    if found_score*100 >= mean*100:
        top_i=i
    else:
        bot_i=i   
    if top_i-bot_i > 1: 
        find_mean_index()    
    
find_mean_index()
mean_index=top_i
percentile_range=int(steam.shape[0]*25/1000)
bot_i=mean_index-percentile_range
top_i=mean_index+percentile_range
bot_score=sorted_steam.loc[bot_i,'store_uscore']
top_score=sorted_steam.loc[top_i,'store_uscore']

sorted_steam=sorted_steam[(sorted_steam['store_uscore'] >= bot_score) & (sorted_steam['store_uscore'] <= top_score)]
sorted_steam.to_csv('steam_mean_5%.csv',index=False)

#%%
## Prix caractéristique d'un jeu à succès.
counts=np.ones_like(steam95.index)/steam95.shape[0]

plt.figure(dpi=300)
plt.hist(steam95['full_price'], bins=range(0, 7000, 500), weights=counts, ec="tomato")
plt.title('Histogramme du prix des jeux à succès sur Steam\n(en centimes)')
plt.show()

#%%
## Répartition du prix des jeux Steam
bins=np.arange(0, 7000, 500)
counts=np.ones_like(steam.index)/steam.shape[0]
clipped_steam=np.clip(steam['full_price'], bins[0], bins[-1])

xbins=np.arange(0, 7000, 1000)
xlabels=xbins[0:].astype(str)
xlabels[-1]+='+'

plt.figure(dpi=300)
plt.hist(clipped_steam, bins=bins, weights=counts, ec="tomato")
plt.xticks(ticks=1000*np.arange(len(xlabels)), labels=xlabels)
plt.title('Histogramme du prix des jeux sur Steam\n(en centimes)')
plt.show()

#%%
## Difficulté caractéristique d'un jeu à succès.
steam95_difficulty=steam95['gfq_difficulty'].dropna()
diffs=['Simple', 'Simple-Easy', 'Easy', 'Easy-Just Right', 'Just Right', 'Just Right-Tough', 'Tough', 'Tough-Unforgiving', 'Unforgiving']
diff_freqs=[]
diffs_size=steam95_difficulty.shape[0]

for diff in diffs:
    diff_size=steam95_difficulty[steam95_difficulty == diff].shape[0]
    diff_freqs.append(diff_size/diffs_size*100)

plt.figure(dpi=300)
plt.bar(diffs, diff_freqs)
plt.xticks(rotation=45, ha="right")
plt.title('Histogramme de la difficulté des jeux à succès (Steam)')
plt.show()

#%%
## Get number of games by tags, for the top 5%.
genres95={}
tags95={}
steamtags=steam95['tags'].dropna()
steamtags=steamtags.reset_index(drop=True)

for i in range(steamtags.shape[0]):
    gametags=steamtags[i]
    gametags=gametags.split(',')

    for tag in gametags:
        if tag not in tags95:
            tags95[tag]=1
        else:
            tags95[tag]+=1

tags95=dict(sorted(tags95.items(), key=lambda item: item[1]))
display(tags95)