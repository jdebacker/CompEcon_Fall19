#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Defining important packages upfront
import pandas as pd
from functools import reduce
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import scipy.stats as stats
import math
import statsmodels.api as sm
from IPython.display import Latex
from IPython.display import Math
import scipy

# Reading in the datafile
df=pd.read_excel('radio_merger_data.xlsx')


# In[2]:


# Creating two seperate datasets for 2007 and 2008, for ease of calculations and recombining them later:

df_2007=df[df['year']==2007]
del df_2007['year']
df_2008=df[df['year']==2008]
del df_2008['year']


# In[3]:


# Seperating out buyer and target data for both years, to create the permutation dataset:
df_2007_buyer=df_2007[['buyer_id','buyer_lat','buyer_long','num_stations_buyer','corp_owner_buyer']]
df_2007_target=df_2007[['target_id','target_lat','target_long','price','hhi_target','population_target']]

df_2008_buyer=df_2008[['buyer_id','buyer_lat','buyer_long','num_stations_buyer','corp_owner_buyer']]
df_2008_target=df_2008[['target_id','target_lat','target_long','price','hhi_target','population_target']]


# In[4]:


# Create a list of matched buyers that will be used to hypothetically exchange targets in the max. score estimation:
list_2007=df_2007_buyer['buyer_id'].unique().tolist()
list_2008=df_2008_buyer['buyer_id'].unique().tolist()

# Importating itertools package to create buyer pairs from the list of buyers for both years
from itertools import combinations

# This part creates a column of pairs
buyer_pairs_2007=pd.DataFrame([",".join(map(str, comb)) for comb in combinations(list_2007, 2)])
buyer_pairs_2008=pd.DataFrame([",".join(map(str, comb)) for comb in combinations(list_2008, 2)])


# Naming the column pairs
buyer_pairs_2007.columns=['Pair']
buyer_pairs_2008.columns=['Pair']


# Splitting the pairs columnn into two columns for paired buyers
buyer_pairs_2007[['buyer1','buyer2']]=buyer_pairs_2007['Pair'].str.split(",",expand=True).astype(str).astype(int)
buyer_pairs_2008[['buyer1','buyer2']]=buyer_pairs_2008['Pair'].str.split(",",expand=True).astype(str).astype(int)


# Deleting the original 'pair' column
del buyer_pairs_2007['Pair']
del buyer_pairs_2008['Pair']

#buyer_pairs_2007['buyer1'].astype(str).astype(int)
#buyer_pairs_2007['buyer2'].astype(str).astype(int)

#buyer_pairs_2008['buyer1'].astype(str).astype(int)
#buyer_pairs_2008['buyer2'].astype(str).astype(int)


# In[5]:


# The 2007 dataset should have 45x44/2= 990 pairs or observations
# The 2008 dataset should have 54x53/2=1431 pairs or observations
print("Number of obs. in 2007 is:",buyer_pairs_2007.shape[0],"and Number of obs. in 2008 is:",buyer_pairs_2008.shape[0])


# In[6]:


# Now for each buyer pair obs., need to pull in the variables required to calculate the max. score estimator
# Since we have two buyers, the respective variables will be appended with _1 and _2 indicating which buyer is referre to

# For 2007
# Buyer characateristics for both pair of buyers
Market1_2007=pd.merge(buyer_pairs_2007, df_2007_buyer, left_on='buyer1',right_on='buyer_id',how='left')
Market2_2007=pd.merge(Market1_2007,df_2007_buyer,left_on='buyer2',right_on='buyer_id',how='left',suffixes=('_1','_2'))
# Target characteristics for both pairs of buyers
Market3_2007=pd.merge(Market2_2007,df_2007_target,left_on='buyer1',right_on='target_id',how='left')
Market4_2007=pd.merge(Market3_2007,df_2007_target,left_on='buyer2',right_on='target_id',how='left',suffixes=('_1','_2'))

# For 2008
# Buyer charactsristics for both pair of buyers
Market1_2008=pd.merge(buyer_pairs_2008, df_2008_buyer, left_on='buyer1',right_on='buyer_id',how='left')
Market2_2008=pd.merge(Market1_2008,df_2008_buyer,left_on='buyer2',right_on='buyer_id',how='left',suffixes=('_1','_2'))
# Target charactsristics for both pair of buyers
Market3_2008=pd.merge(Market2_2008,df_2008_target,left_on='buyer1',right_on='target_id',how='left')
Market4_2008=pd.merge(Market3_2008,df_2008_target,left_on='buyer2',right_on='target_id',how='left',suffixes=('_1','_2'))


# In[7]:


# Calculate the distances for observed and couterfactual buyer-targets
import geopy
from geopy.distance import vincenty

# For 2007
# Distance of first buyer pair and its original target
for index, row in Market4_2007.iterrows():
    Distance11=geopy.distance.geodesic((row['buyer_lat_1'],row['buyer_long_1']), (row['target_lat_1'],row['target_long_1'])).miles
    Market4_2007.set_value(index, 'Distance11',Distance11)

# Distance of second buyer pair and its original target
for index, row in Market4_2007.iterrows():
    Distance22=geopy.distance.geodesic((row['buyer_lat_2'],row['buyer_long_2']), (row['target_lat_2'],row['target_long_2'])).miles
    Market4_2007.set_value(index, 'Distance22',Distance22)

# Distance of first buyer pair and its counterfactual target (original target of second of buyer pair)
for index, row in Market4_2007.iterrows():
    Distance12=geopy.distance.geodesic((row['buyer_lat_1'],row['buyer_long_1']), (row['target_lat_2'],row['target_long_2'])).miles
    Market4_2007.set_value(index, 'Distance12',Distance12)

# Distance of second buyer pair and its counterfactual target (original target of first of buyer pair)
for index, row in Market4_2007.iterrows():
    Distance21=geopy.distance.geodesic((row['buyer_lat_2'],row['buyer_long_2']), (row['target_lat_1'],row['target_long_1'])).miles
    Market4_2007.set_value(index, 'Distance21',Distance21)


    

# For 2008

# Distance of first buyer pair and its original target
for index, row in Market4_2008.iterrows():
    Distance11=geopy.distance.geodesic((row['buyer_lat_1'],row['buyer_long_1']), (row['target_lat_1'],row['target_long_1'])).miles
    Market4_2008.set_value(index, 'Distance11',Distance11)

# Distance of second buyer pair and its original target
for index, row in Market4_2008.iterrows():
    Distance22=geopy.distance.geodesic((row['buyer_lat_2'],row['buyer_long_2']), (row['target_lat_2'],row['target_long_2'])).miles
    Market4_2008.set_value(index, 'Distance22',Distance22)

# Distance of first buyer pair and its counterfactual target (original target of second of buyer pair)
for index, row in Market4_2008.iterrows():
    Distance12=geopy.distance.geodesic((row['buyer_lat_1'],row['buyer_long_1']), (row['target_lat_2'],row['target_long_2'])).miles
    Market4_2008.set_value(index, 'Distance12',Distance12)
    
# Distance of second buyer pair and its counterfactual target (original target of first of buyer pair)
for index, row in Market4_2008.iterrows():
    Distance21=geopy.distance.geodesic((row['buyer_lat_2'],row['buyer_long_2']), (row['target_lat_1'],row['target_long_1'])).miles
    Market4_2008.set_value(index, 'Distance21',Distance21)



# In[8]:


# Now I calculate the variables used in the inquality used for max. score estimation

# Also, since I have calculated the pairs in 2007 and 2008 market, I append those dataframes to form a single dataframe:
Market=Market4_2007.append(Market4_2008, ignore_index=True)


# In[9]:


# Defining the Maximum Score Estimator Function:

def MSE(params, data):
    '''
    Args for this function are the data and initial parameter guess (not req. for differential evolution)
    '''
    alpha, beta=params[0], params[1]
    MSE=0
    
    '''
    LHS1 and LHS2 are the value of observed merger values for buyer1 and 2 respectively 
    These two form the left hand side of the MSE inquality
    
    RHS1 and RHS2 are the value of counterfactual merger (buyer 1 with buyer 2's target and buyer 2 with buyer 1's target)
    These two form the right hand side of the MSE inquality
    '''
    
    for index, row in data.iterrows():
        LHS1= row['num_stations_buyer_1'] * row['population_target_1'] + alpha * row['corp_owner_buyer_1'] * row['population_target_1'] +  beta * row['Distance11'] 
        
        LHS2= row['num_stations_buyer_2'] * row['population_target_2'] + alpha * row['corp_owner_buyer_2'] * row['population_target_2'] + beta * row['Distance22']
        
        LHS=LHS1 + LHS2
        
        
        RHS1= row['num_stations_buyer_1'] * row['population_target_2'] + alpha * row['corp_owner_buyer_1'] * row['population_target_2'] + beta * row['Distance12'] 
        
        RHS2= row['num_stations_buyer_2'] * row['population_target_1'] + alpha * row['corp_owner_buyer_2'] * row['population_target_1'] + beta * row['Distance21']
        
        RHS=RHS1 + RHS2
        
        '''
        If the value of observed mergers (LHS) is greater than couterfactual mergers (RHS), the MSE increassed by 1
        and since I minizmize the score, I use -1*MSE
        '''
        
        if LHS >= RHS:
            MSE= MSE + 1
            
    return(-1*MSE)

        


# In[45]:


# Using Nelder-Mead for part 1
param_guess=(1700, 1700)
results1_NM=minimize(MSE, param_guess,
                 method='Nelder-Mead',
                 args=(Market),
                 options={'disp':True})


# In[46]:


results1_NM.x


# In[69]:


# Using Differential Evolution for part 1
results1_DE=scipy.optimize.differential_evolution(MSE, strategy='best1bin',args=(Market, ),bounds=[(-30000,30000),(-30000,30000)])


# In[70]:


results1_DE


# In[10]:


# Defining the Maximum Score Estimator Function with transfer:

def MSE_transfer(params, data):
    delta, alpha, gamma, beta= params[0], params[1], params[2], params[3]
    MSE=0
    '''
    LHS1 and LHS2 are the value of observed merger values for buyer1 and 2 respectively 
    These two form the left hand side of the MSE inquality
    Simialr to the MSE, but this time included the HHI and also parameterized the first term
    
    RHS1 and RHS2 are the value of counterfactual merger (buyer 1 with buyer 2's target and buyer 2 with buyer 1's target)
    These two form the right hand side of the MSE inquality
    Simialr to the MSE, but this time included the HHI and also parameterized the first term
    '''
    
    
    for index, row in data.iterrows():
        LHS1= delta * row['num_stations_buyer_1'] * row['population_target_1'] + alpha * row['corp_owner_buyer_1'] * row['population_target_1'] + gamma * row['hhi_target_1'] + beta * row['Distance11'] 
        
        LHS2= delta * row['num_stations_buyer_2'] * row['population_target_2'] + alpha * row['corp_owner_buyer_2'] * row['population_target_2'] + gamma * row['hhi_target_2'] + beta * row['Distance22']
        
        
        
        RHS1= delta * row['num_stations_buyer_1'] * row['population_target_2'] + alpha * row['corp_owner_buyer_1'] * row['population_target_2'] + gamma * row['hhi_target_2'] + beta * row['Distance12'] 
        
        RHS2= delta * row['num_stations_buyer_2'] * row['population_target_1'] + alpha * row['corp_owner_buyer_2'] * row['population_target_1'] + gamma * row['hhi_target_1'] + beta * row['Distance21']
        
        '''
        Similar value comparison of observed and counterfactual mergers, just that the transfer pricing condition 
        is also included. This means that if 
        1) the difference in merger value between buyer 1's observed and couterfactual merger
        is greater than the price it differential of observed and counterfactual merger
        2) the difference in merger value between buyer 2's observed and counterfactual merger
        is greater than the price differential of oberved and counterfactual merger, then
        the parameters satisfy the MSE inquality
        '''
        
        if ((LHS1 - RHS1) >= (row['price_1'] - row['price_2'])) & ((LHS2 - RHS2) >= (row['price_2'] - row['price_1'])):
            MSE= MSE + 1
            
    return( -1 * MSE)

        


# In[17]:


# Using Differential Evolution for part 2 ( price transfers)
import scipy
results2_DE=scipy.optimize.differential_evolution(MSE, strategy='best1bin',args=(Market, ),bounds=[(-20000,20000),(-30000,30000),(-20000,20000),(-30000,30000)])


# In[18]:


results2_DE


# In[ ]:




