# Saharnaz Babaei
# Problem Set 4

# Note for later: A package for solving matching games: https://pypi.org/project/matching/
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from pandas import ExcelWriter
from pandas import ExcelFile
import itertools
import scipy.optimize as opt
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
# easy_install pip
# In command prompt: <pip install geopy> - if failed: https://stackoverflow.com/questions/36064495/importerror-no-module-named-geopy-ipython-notebook
import geopy
from geopy import distance
#geopy.distance.vincenty: Deprecated since version 1.13: Vincenty will be removed in geopy 2.0. ref.: https://geopy.readthedocs.io/en/stable/#module-geopy.distance


# '''
# My sketch for solving the problem:
# - Read data
# - Prepare data
#     - Convert scale of price and population to 1000 dollars and 1000 people respectively;
#     - Two different datasets for each year;
#     - Create counterfactual and factual mergers' dataset;
#     - Create distance for mergers.
#     - a note for myself: https://datacarpentry.org/python-ecology-lesson/03-index-slice-subset/
# - def score function (for 2 different models):
#     - without transfer (GS algorithm);
#     - with transfers (BSS algorithm)
# - Optimize score functions and obtain the desired parameters
# '''

df = pd.read_excel("radio_merger_data.xlsx")
df.head()

df['price'] = df['price']/1000
df['population_target'] = df['population_target']/1000

'''
#The number of all possible combinations:
num_comb = len(list(itertools.product(df2007.buyer_id.tolist(), df2007.target_id.tolist()))) + len(list(itertools.product(df2008.buyer_id.tolist(), df2008.target_id.tolist())))
# Any possible combination (match) between the buyer and target (including real/factual and counterfactual data):
B2007 = df2007.loc[:, ['year', 'buyer_id', 'buyer_lat', 'buyer_long', 'num_stations_buyer', 'corp_owner_buyer']]
B2008 = df2008.loc[:, ['year', 'buyer_id', 'buyer_lat', 'buyer_long', 'num_stations_buyer', 'corp_owner_buyer']]
T2007 = df2007.loc[:, ['target_id', 'target_lat', 'target_long', 'price', 'hhi_target', 'population_target']]
T2008 = df2008.loc[:, ['target_id', 'target_lat', 'target_long', 'price', 'hhi_target', 'population_target']]
def cartesian_prod7(B2007, T2007):
    return(B2007.assign(key=1).merge(T2007.assign(key=1), on='key').drop('key', 1))
combinations_2007 = cartesian_prod7(B2007, T2007)
def cartesian_prod8(B2008, T2008):
    return(B2008.assign(key=1).merge(T2008.assign(key=1), on='key').drop('key', 1))
combinations_2008 = cartesian_prod8(B2008, T2008)
'''
'''
Due to lack of time, could not get rid of factual data; so used another method to get counterfactual dataset.
I will work on that later to remove common data in this cartesian data with my dataframe which is actually the factual dataset.
'''
dfy = dict(iter(df.groupby('year', as_index = False)))
dfy[2007].describe().to_csv("describe2007.csv")
dfy[2008].describe().to_csv("describe2008.csv")
B = ['year', 'buyer_id', 'buyer_lat', 'buyer_long', 'num_stations_buyer', 'corp_owner_buyer']
T = ['target_id', 'target_lat', 'target_long', 'price', 'hhi_target', 'population_target']
data = [pd.DataFrame(dfy[2007]), pd.DataFrame(dfy[2008])]
counterfact = pd.DataFrame()
counterfact = pd.DataFrame([x[B].iloc[i].values.tolist() + x[T].iloc[j].values.tolist() for x in data for i in range(len(x)) for j in range(len(x)) if i!= j], columns = B + T)

# http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/
def dist(d):
    '''
    This function calculates distance between two points.
    b_loc = The coordinates for buyer's location
    t_loc = The coordinates for target's location
    The result is in miles.
    '''
    b_loc = (d['buyer_lat'], d['buyer_long'])
    t_loc = (d['target_lat'], d['target_long'])
    return distance.distance(b_loc, t_loc).miles

df['distance'] = df.apply(dist, axis=1)
counterfact['distance'] = counterfact.apply(dist, axis=1)

df2007 = df[df['year'] == 2007]
df2008 = df[df['year'] == 2008]
cf2007 = counterfact[counterfact['year']==2007]
cf2008 = counterfact[counterfact['year']==2008]

def score1_GS(params, m, n):
    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = x_1bm * y_1tm + alpha * x_2bm * y_1tm + beta * distance_btm + epsilon_btm
    payoff to merger = (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t
    '''
    f_b_t = m['num_stations_buyer'] * m['population_target'] + params[0] * m['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_cb_ct = n['num_stations_buyer'] * n['population_target'] + params[0] * n['corp_owner_buyer'] * n['population_target'] + params[1] * n['distance']
    f_cb_t = n['num_stations_buyer'] * m['population_target'] + params[0] * n['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_b_ct = m['num_stations_buyer'] * n['population_target'] + params[0] * m['corp_owner_buyer'] * n['population_target'] + params[1] * m['distance']
    L = f_b_t + f_cb_ct
    R = f_cb_t + f_b_ct
    indicator=(L>R)
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10)]
GS1_dif_2007 = differential_evolution(score1_GS, bounds, args=(df2007, cf2007), strategy='best1bin', maxiter=10000)
GS1_dif_2008 = differential_evolution(score1_GS, bounds, args=(df2008, cf2008), strategy='best1bin', maxiter=10000)

def scoreT1_GS(params, m, n):
    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = x_1bm * y_1tm + alpha * x_2bm * y_1tm + beta * distance_btm + epsilon_btm
    payoff to merger = (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t
    '''
    f_b_t = m['num_stations_buyer'] * m['population_target'] + params[0] * m['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_cb_ct = n['num_stations_buyer'] * n['population_target'] + params[0] * n['corp_owner_buyer'] * n['population_target'] + params[1] * n['distance']
    f_cb_t = n['num_stations_buyer'] * m['population_target'] + params[0] * n['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_b_ct = m['num_stations_buyer'] * n['population_target'] + params[0] * m['corp_owner_buyer'] * n['population_target'] + params[1] * m['distance']
    L = f_b_t + f_cb_ct
    R = f_cb_t + f_b_ct
    indicator=(L>R)
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10)]
GST1_dif = differential_evolution(scoreT1_GS, bounds, args=(df, counterfact), strategy='best1bin', maxiter=10000)

def score2_GS(params, m, n):

    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = delta * x_1bm * y_1tm + alpha * x_2bm * y_1tm + gamma* HHI_tm + beta * distance_btm + epsilon_btm
    payoff to merger = delta * (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + gamma * (market concentration index) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t

    '''
    f_b_t = params[0] * m['num_stations_buyer'] * m['population_target'] + params[1] * m['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_cb_ct = params[0] * n['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2]*n['hhi_target'] + params[3] * n['distance']
    f_cb_t = params[0] * n['num_stations_buyer'] * m['population_target'] + params[1] * n['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_b_ct = params[0] * m['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']

    L = f_b_t + f_cb_ct
    R = f_cb_t + f_b_ct
    indicator=(L>R)
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10), (-10, 10), (-10,10)]
GS2_dif_2007 = differential_evolution(score2_GS, bounds, args=(df2007, cf2007), strategy='best1bin', maxiter=10000)
GS2_dif_2008 = differential_evolution(score2_GS, bounds, args=(df2008, cf2008), strategy='best1bin', maxiter=10000)

def scoreT2_GS(params, m, n):

    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = delta * x_1bm * y_1tm + alpha * x_2bm * y_1tm + gamma* HHI_tm + beta * distance_btm + epsilon_btm
    payoff to merger = delta * (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + gamma * (market concentration index) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t

    '''
    f_b_t = params[0] * m['num_stations_buyer'] * m['population_target'] + params[1] * m['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_cb_ct = params[0] * n['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2]*n['hhi_target'] + params[3] * n['distance']
    f_cb_t = params[0] * n['num_stations_buyer'] * m['population_target'] + params[1] * n['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_b_ct = params[0] * m['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']

    L = f_b_t + f_cb_ct
    R = f_cb_t + f_b_ct
    indicator=(L>R)
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10), (-10, 10), (-10,10)]
GST2_dif = differential_evolution(scoreT2_GS, bounds, args=(df, counterfact), strategy='best1bin', maxiter=10000)

def score1_BSS(params, m, n):
    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = x_1bm * y_1tm + alpha * x_2bm * y_1tm + beta * distance_btm + epsilon_btm
    payoff to merger = (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t
    '''
    f_b_t = m['num_stations_buyer'] * m['population_target'] + params[0] * m['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_cb_ct = n['num_stations_buyer'] * n['population_target'] + params[0] * n['corp_owner_buyer'] * n['population_target'] + params[1] * n['distance']
    f_cb_t = n['num_stations_buyer'] * m['population_target'] + params[0] * n['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_b_ct = m['num_stations_buyer'] * n['population_target'] + params[0] * m['corp_owner_buyer'] * n['population_target'] + params[1] * m['distance']
    L1 = f_b_t - f_b_ct
    R1 = m['price'] - n['price']
    L2 = f_cb_ct - f_cb_t
    R2 = n['price'] - m['price']
    indicator= ((L1 >= R1) & (L2 >= R2))
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10)]
BSS1_dif_2007 = differential_evolution(score1_BSS, bounds, args=(df2007, cf2007), strategy='best1bin', maxiter=10000)
BSS1_dif_2008 = differential_evolution(score1_BSS, bounds, args=(df2008, cf2008), strategy='best1bin', maxiter=10000)

def scoreT1_BSS(params, m, n):
    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = x_1bm * y_1tm + alpha * x_2bm * y_1tm + beta * distance_btm + epsilon_btm
    payoff to merger = (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t
    '''
    f_b_t = m['num_stations_buyer'] * m['population_target'] + params[0] * m['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_cb_ct = n['num_stations_buyer'] * n['population_target'] + params[0] * n['corp_owner_buyer'] * n['population_target'] + params[1] * n['distance']
    f_cb_t = n['num_stations_buyer'] * m['population_target'] + params[0] * n['corp_owner_buyer'] * m['population_target'] + params[1] * m['distance']
    f_b_ct = m['num_stations_buyer'] * n['population_target'] + params[0] * m['corp_owner_buyer'] * n['population_target'] + params[1] * m['distance']
    L1 = f_b_t - f_b_ct
    R1 = m['price'] - n['price']
    L2 = f_cb_ct - f_cb_t
    R2 = n['price'] - m['price']
    indicator= ((L1 >= R1) & (L2 >= R2))
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10)]
BSST1_dif = differential_evolution(scoreT1_BSS, bounds, args=(df, counterfact), strategy='best1bin', maxiter=10000)

def score2_BSS(params, m, n):
    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = delta * x_1bm * y_1tm + alpha * x_2bm * y_1tm + gamma* HHI_tm + beta * distance_btm + epsilon_btm
    payoff to merger = delta * (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + gamma * (market concentration index) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t

    '''
    f_b_t = params[0] * m['num_stations_buyer'] * m['population_target'] + params[1] * m['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_cb_ct = params[0] * n['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2]*n['hhi_target'] + params[3] * n['distance']
    f_cb_t = params[0] * n['num_stations_buyer'] * m['population_target'] + params[1] * n['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_b_ct = params[0] * m['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']

    L1 = f_b_t - f_b_ct
    R1 = m['price'] - n['price']
    L2 = f_cb_ct - f_cb_t
    R2 = n['price'] - m['price']
    indicator= ((L1 >= R1) & (L2 >= R2))
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10), (-10, 10), (-10,10)]
BSS2_dif_2007 = differential_evolution(score2_BSS, bounds, args=(df2007, cf2007), strategy='best1bin', maxiter=10000)
BSS2_dif_2008 = differential_evolution(score2_BSS, bounds, args=(df2008, cf2008), strategy='best1bin', maxiter=10000)

def scoreT2_BSS(params, m, n):
    '''
    This function calculates the payoff function for mergers to be used in the indicator function.
    Indicator == 1 if f(b,t) + f(b',t') > f(b',t) + f(b,t')
    Indicator == 0 otherwise.
    f(b,t,m) = delta * x_1bm * y_1tm + alpha * x_2bm * y_1tm + gamma* HHI_tm + beta * distance_btm + epsilon_btm
    payoff to merger = delta * (number of stations owned) * (population in range of target) + alpha * (indicator for corporate ownership) * (population in range of target) + gamma * (market concentration index) + beta * (distance bwbuyer and target) + (error term)
    market m == 2007 & 2008
    buyer b
    target t

    '''
    f_b_t = params[0] * m['num_stations_buyer'] * m['population_target'] + params[1] * m['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_cb_ct = params[0] * n['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2]*n['hhi_target'] + params[3] * n['distance']
    f_cb_t = params[0] * n['num_stations_buyer'] * m['population_target'] + params[1] * n['corp_owner_buyer'] * m['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']
    f_b_ct = params[0] * m['num_stations_buyer'] * n['population_target'] + params[1] * n['corp_owner_buyer'] * n['population_target'] + params[2] * m['hhi_target'] + params[3] * m['distance']

    L1 = f_b_t - f_b_ct
    R1 = m['price'] - n['price']
    L2 = f_cb_ct - f_cb_t
    R2 = n['price'] - m['price']
    indicator= ((L1 >= R1) & (L2 >= R2))
    total_payoff = indicator.sum()
    return -total_payoff

bounds = [(-5,5), (-10,10), (-10, 10), (-10,10)]
BSST2_dif = differential_evolution(scoreT2_BSS, bounds, args=(df, counterfact), strategy='best1bin', maxiter=10000)

print('Estimated Parameters for Model 1, without transfers, using Gale-Shapely Algorithm for Market = 2007: \n', GS1_dif_2007.x)
print('Estimated Parameters for Model 1, without transfers, using Gale-Shapely Algorithm for Market = 2008: \n', GS1_dif_2008.x)
print('Estimated Parameters for Model 2, without transfers, using Gale-Shapely Algorithm for Market = 2007: \n', GS2_dif_2007.x)
print('Estimated Parameters for Model 2, without transfers, using Gale-Shapely Algorithm for Market = 2008: \n', GS2_dif_2008.x)
print('Estimated Parameters for Model 1, with transfers, using Becker-Shapely-Subik Algorithm for Market = 2007: \n', BSS1_dif_2007.x)
print('Estimated Parameters for Model 1, with transfers, using Becker-Shapely-Subik Algorithm for Market = 2008: \n', BSS1_dif_2008.x)
print('Estimated Parameters for Model 2, with transfers, using Becker-Shapely-Subik Algorithm for Market = 2007: \n', BSS2_dif_2007.x)
print('Estimated Parameters for Model 2, with transfers, using Becker-Shapely-Subik Algorithm for Market = 2007: \n', BSS2_dif_2008.x)
#####################################################################################################################
print('Estimated Parameters for Model 1, without transfers, using Gale-Shapely Algorithm: \n', GST1_dif.x)
print('Estimated Parameters for Model 2, without transfers, using Gale-Shapely Algorithm: \n', GST2_dif.x)
print('Estimated Parameters for Model 1, with transfers, using Becker-Shapely-Subik Algorithm: \n', BSST1_dif.x)
print('Estimated Parameters for Model 2, with transfers, using Becker-Shapely-Subik Algorithm: \n', BSST2_dif.x)
