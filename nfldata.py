# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 18:24:59 2022

@author: seanh
"""

#%% Initialize

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

#%%
""" creating a class for getting the nfl data and doing some data cleaning """
class nfl_data:
    
    """ ask for the file location """
    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()
        self.df = pd.read_csv(filepath)
    
    """ get a single row of all the games so we can do some of our analysis 
    with a lighter data frame """
    def singlegamedata(self):
        game_ids = self.df.game_id.unique()
        game_list = game_ids.tolist()
        singlerowdf = self.df.drop_duplicates(subset=['game_id'])
        return singlerowdf
        
    def bettingline(self,singledf):
        betdf = singledf[['game_id','team','Roof','Surface','Temperature',
                          'Humidity','Wind_Speed','Vegas_Line',
                          'Vegas_Favorite','Over_Under','game_date',
                          'vis_score','home_score']]
        
        """ calculate the overall score, differential, and if the points
        total was covered """
        pointdif = []
        pointtotal = []
        covered = []
        for index,row in betdf.iterrows():
            pointdif.append(row['home_score'] - row['vis_score'])
            pointtotal.append(row['home_score'] + row['vis_score'])
            if (row['home_score'] + row['vis_score']) > row['Over_Under']:
                covered.append('Yes')
            elif (row['home_score'] + row['vis_score']) < row['Over_Under']:
                covered.append('No')
            elif (row['home_score'] + row['vis_score']) == row['Over_Under']:
                covered.append('Push')
        
        """ add the new columns to the dataframe """
        betdf = betdf.assign(pointdif=pointdif,pointtotal=pointtotal,
                             covered=covered)
        
        return betdf
    

nfldata = nfl_data()
singlerowdf = nfldata.singlegamedata()
betdf = nfldata.bettingline(singlerowdf)
    

        
