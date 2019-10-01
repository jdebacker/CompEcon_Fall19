# Saharnaz Babaei Balderlou
# Problem Set 3
#------------------------------------------------------------------------------
# Import required packages
#------------------------------------------------------------------------------
import pandas as pd # will be used to read .dta file by .read_stata()
import numpy as np
import matplotlib.pyplot as plt # will be used to see the obvious relationship of desired variables in a scatterplot
#%matplotlib inline
import math # to use in some equations
from scipy.optimize import minimize # for optimization of Likelihood function (MLE method)
import scipy.optimize as opt
import statsmodels.api as statmod
import scipy.stats as stats

#------------------------------------------------------------------------------
# Read data and prepare to utilize (Part 1 & 2)
#------------------------------------------------------------------------------
df1 = pd.read_stata('PS3_data.dta')
# My note for later: https://www.shanelynn.ie/using-pandas-dataframe-creating-editing-viewing-data-in-python/
print("Dataframe: ")
df1.head()
'''
hlabinc = annual labor income of the head
hannhrs = annual hours of the head
hsex = gender of the head (1 = Male, 2 = Female)
hrace = race of the head (1 = white, 2 = Black, 3 = Native American, 4 = Asian/Pacific Islander, 5 = Hispanic, 6,7 = Other)
age = age of the head
hyrsed = years of education of the head
'''
print("Data Statistics:")
df1.describe()
print("Scatterplot between annual labor inome of the head and years of education of the head")
plt.style.use('seaborn')
df1.plot(x = 'hyrsed', y = 'hlabinc', kind = 'scatter')
plt.show()
plt.savefig('scat_inc_edu.png')
#drop missing values
df1_subset = df1.dropna(how = 'any', subset = ['hlabinc', 'hannhrs', 'hsex', 'hrace', 'age', 'hyrsed'])
df1_subset.describe()
# select male heads of HH whose age is between 25 & 60 (included!), and wage > $7/hr
df2 = df1_subset[['id68', 'year', 'intid', 'hlabinc', 'hannhrs', 'hsex', 'hrace', 'age', 'hyrsed']]
df2['annhrs'] = df2['hannhrs'].where(df2['hannhrs']>0)
df2['hrwage'] = df2['hlabinc']/df2['annhrs'] # compute hourly wage
df2 = df2[(df2.hsex == 1.0) & (df2.age >= 25) & (df2.age <= 60) & (df2.hrwage > 7)] #Part 1
df2['ln_hrwage'] = np.log(df2['hrwage']) #log of wages
df2.describe()
# This is a note for me: https://stackoverflow.com/questions/11587782/creating-dummy-variables-in-pandas-for-python
race_dummy = pd.get_dummies(df2['hrace']) # Defining race dummies (There is no Hispanic individual in dataset)
df2['constant'] = 1
data = pd.concat([df2, race_dummy], axis = 1)
data.rename(columns = {1.0: 'White', 2.0: 'Black', 3.0: 'Others'}, inplace = True) #final data "data"; ready to estimate model
data.head()
data.dtypes

# Save the data
np.save("data", data)
# Separate years for estimation
data1971 = data[data['year'] == 1971]
np.save("data1971", data1971)
data1980 = data[data['year'] == 1980]
np.save("data1980", data1980)
data1990 = data[data['year'] == 1990]
np.save("data1990", data1990)
data2000 = data[data['year'] == 2000]
np.save("data2000", data2000)

#------------------------------------------------------------------------------
# ML estimation (Part 3)
#------------------------------------------------------------------------------
'''
ln(w_it) = alpha + beta_1 * Educ_it + beta_2 * Age_it + beta_3 * Black_it + beta_4 * Hispanic_it + beta_5 * OtherRace_it + epsilon_it
w_it = wage of individual i in survey year t
Educ_it = education in years
Age_it = age in years
Black_it, Hispanic_it, OtherRace_it = dummy variables for race = Black, Hispanic, Not (belongs to {White, Black, Hispanic})
'''

# Define my objective function
def myLL(params, t):
    # Coeff.s
    beta0, beta1, beta2, beta3, beta4, sigma = params
    beta = np.array([beta0, beta1, beta2, beta3, beta4])
    n = len(t)
    # Independent variables matrix (No Hispanic)
    x0 = np.array(t['constant']).astype('float')
    x1 = np.array(t['hyrsed']).astype('float')
    x2 = np.array(t['age']).astype('float')
    x3 = np.array(t['Black']).astype('float')
    x4 = np.array(t['Others']).astype('float')
    X = np.column_stack((x0, x1, x2, x3, x4))
    # Dependent variable matrix
    y = np.array(t['ln_hrwage']).astype('float')
    y_bar = np.dot(X, beta)
    ll = (-(n/2)*np.log(2*np.pi) - (n/2)*np.log(sigma**2) - (1/(2*sigma**2))*((y-y_bar).T @ (y - y_bar)))
    return (-ll)

# MLE; 'Nelder-Mead'
nbeta = 5
beta = np.zeros(nbeta)
beta0 = 0.1
beta1 = 0.1
beta2 = 0.1
beta3 = 0.1
beta4 = 0.1
sigma = 0.1
beta = [beta0, beta1, beta2, beta3, beta4]
params = [beta0, beta1, beta2, beta3, beta4, sigma]

bounds = ((1e-10, None), (None,None), (None,None), (None,None), (None,None), (None,None))

res_NM = opt.minimize(myLL, params, args=(data), method='Nelder-Mead', bounds=bounds)
print("MLE coefficients: ", "Total dataset")
print("=============================")
print(res_NM)
print("_____________________________________")
res71_NM = opt.minimize(myLL, params, args=(data1971), method='Nelder-Mead', bounds=bounds)
print("MLE coefficients: ", "year == 1971")
print("=============================")
print(res71_NM)
print("_____________________________________")
res80_NM = opt.minimize(myLL, params, args=(data1980), method='Nelder-Mead', bounds=bounds)
print("MLE coefficients: ", "year == 1980")
print("=============================")
print(res80_NM)
print("_____________________________________")
res90_NM = opt.minimize(myLL, params, args=(data1990), method='Nelder-Mead', bounds=bounds)
print("MLE coefficients: ", "year == 1990")
print("=============================")
print(res90_NM)
print("_____________________________________")
res2000_NM = opt.minimize(myLL, params, args=(data2000), method='Nelder-Mead', bounds=bounds)
print("MLE coefficients: ", "year == 2000")
print("=============================")
print(res2000_NM)
print("_____________________________________")
'''
years = ["data1971.npy", "data1980.npy", "data1990.npy", "data2000.npy", "data.npy"]
for t in years:
    res_MLE = opt.minimize(myLL, params, args=(t), method='Nelder-Mead', bounds=bounds)
    print("MLE coefficients: ", t)
    print(res_MLE)
    print("_____________________________________")
#### I tried this loop so many times and attempted to troubleshoot but finally I got this error: "string indices must be integers"
'''

# MLE; 'L-BFGS-B'
nbeta = 5
beta = np.zeros(nbeta)
beta0 = 0.1
beta1 = 0.1
beta2 = 0.1
beta3 = 0.1
beta4 = 0.1
sigma = 0.1
beta = [beta0, beta1, beta2, beta3, beta4]
params = [beta0, beta1, beta2, beta3, beta4, sigma]

bounds = ((1e-10, None), (None,None), (None,None), (None,None), (None,None), (None,None))

res_B = opt.minimize(myLL, params, args=(data), method='L-BFGS-B', bounds=bounds)
print("MLE coefficients: ", "Total dataset")
print("=============================")
print(res_B)
print("_____________________________________")
res71_B = opt.minimize(myLL, params, args=(data1971), method='L-BFGS-B', bounds=bounds)
print("MLE coefficients: ", "year == 1971")
print("=============================")
print(res71_B)
print("_____________________________________")
res80_B = opt.minimize(myLL, params, args=(data1980), method='L-BFGS-B', bounds=bounds)
print("MLE coefficients: ", "year == 1980")
print("=============================")
print(res80_B)
print("_____________________________________")
res90_B = opt.minimize(myLL, params, args=(data1990), method='L-BFGS-B', bounds=bounds)
print("MLE coefficients: ", "year == 1990")
print("=============================")
print(res90_B)
print("_____________________________________")
res2000_B = opt.minimize(myLL, params, args=(data2000), method='L-BFGS-B', bounds=bounds)
print("MLE coefficients: ", "year == 2000")
print("=============================")
print(res2000_B)
print("_____________________________________")

# MLE; 'SLSQP'
nbeta = 5
beta = np.zeros(nbeta)
beta0 = 1.20
beta1 = 0.11
beta2 = 0.01
beta3 = 0.20
beta4 = 0.01
sigma = 0.50
beta = [beta0, beta1, beta2, beta3, beta4]
params = [beta0, beta1, beta2, beta3, beta4, sigma]

bounds = ((1e-10, None), (None,None), (None,None), (None,None), (None,None), (None,None))

res_S = opt.minimize(myLL, params, args=(data), method='SLSQP', bounds=bounds)
print("MLE coefficients: ", "Total dataset")
print("=============================")
print(res_S)
print("_____________________________________")
res71_S = opt.minimize(myLL, params, args=(data1971), method='SLSQP', bounds=bounds)
print("MLE coefficients: ", "year == 1971")
print("=============================")
print(res71_S)
print("_____________________________________")
res80_S = opt.minimize(myLL, params, args=(data1980), method='SLSQP', bounds=bounds)
print("MLE coefficients: ", "year == 1980")
print("=============================")
print(res80_S)
print("_____________________________________")
res90_S = opt.minimize(myLL, params, args=(data1990), method='SLSQP', bounds=bounds)
print("MLE coefficients: ", "year == 1990")
print("=============================")
print(res90_S)
print("_____________________________________")
res2000_S = opt.minimize(myLL, params, args=(data2000), method='SLSQP', bounds=bounds)
print("MLE coefficients: ", "year == 2000")
print("=============================")
print(res2000_S)
print("_____________________________________")

# Comparing the MLE coefficients for 3 different methods:
print("All data; Nelder-Mead: ", res_NM.x)
print("1971; Nelder-Mead: ", res71_NM.x)
print("1980; Nelder-Mead: ", res80_NM.x)
print("1990; Nelder-Mead: ", res90_NM.x)
print("2000; Nelder-Mead: ", res2000_NM.x)
print("____________________________________________")
print("All data; L-BFGS-B: ", res_B.x)
print("1971; L-BFGS-B: ", res71_B.x)
print("1980; L-BFGS-B: ", res80_B.x)
print("1990; L-BFGS-B: ", res90_B.x)
print("2000; L-BFGS-B: ", res2000_B.x)
print("____________________________________________")
print("All data; SLSQP: ", res_S.x)
print("1971; L-BFGS-B: ", res71_S.x)
print("1980; L-BFGS-B: ", res80_S.x)
print("1990; L-BFGS-B: ", res90_S.x)
print("2000; L-BFGS-B: ", res2000_S.x)

# OLS
#https://lectures.quantecon.org/py/ols.html
# to estimate each year separately
res_OLS = statmod.OLS(endog=data['ln_hrwage'], exog=data[['constant', 'hyrsed', 'age', 'Black', 'Others']]).fit()
res71_OLS = statmod.OLS(endog=data1971['ln_hrwage'], exog=data1971[['constant', 'hyrsed', 'age', 'Black', 'Others']]).fit()
res80_OLS = statmod.OLS(endog=data1980['ln_hrwage'], exog=data1980[['constant', 'hyrsed', 'age', 'Black', 'Others']]).fit()
res90_OLS = statmod.OLS(endog=data1990['ln_hrwage'], exog=data1990[['constant', 'hyrsed', 'age', 'Black', 'Others']]).fit()
res2000_OLS = statmod.OLS(endog=data2000['ln_hrwage'], exog=data2000[['constant', 'hyrsed', 'age', 'Black', 'Others']]).fit()

print('OLS; Full Sample')
print('===================')
print(res_OLS.summary())
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('OLS; year == 1971')
print('===================')
print(res71_OLS.summary())
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('OLS; year == 1980')
print('===================')
print(res80_OLS.summary())
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('OLS; year == 1990')
print('===================')
print(res90_OLS.summary())
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('OLS; year == 2000')
print('===================')
print(res2000_OLS.summary())
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
'''

years = ['data1971.npy', 'data1980.npy', 'data1990.npy', 'data2000.npy', 'data.npy']
for t in years:
    print('OLS for', t)
    print('===================')
    print(statmod.OLS(endog=t['ln_hrwage'], exog=t[['constant', 'hyrsed', 'age', 'Black', 'Others']]).fit().summary())
    print('_______________________________________________________________________________________________')
'''

#  ---------------------------------
# # Interpretation (Part 4)
#  ---------------------------------
# To answer this question that how the returns to education change over time in these data, we can note that it is increasing. The results for OLS estimation in the full sample indicate that 1 unit increase in the years of education of males will result in a 7.8 % increase in their wages. Using data for 1971, we can see that this increase in the wage is as much as 6.7% as a result of each year of increased education for the male heads. We can also see that the percentage of increase in the wages is 6.8%, 9.8%, & 11% for 1980, 1990, and 2000, respectively, after one more year of education.
#
# In addition, I estimated the same linear model using the maximum likelihood model and the estimated coefficients for the education are 7.8, 6.97, 6.7, 11.8, 10.9 percent for the full sample, 1971 sample of the data, 1980, 1990 and 2000 samples, respectively, which supports the estimation of the model using OLS both in magnitude and signature. MLE method can be estimated using several optimization methods for the likelihood function. After using Nelder-Mead method and gaining aforementioned estimations, we used bounded L-BFGS-B and SLSQP methods. The former estimates the coefficients of the education as 7.8, 6.7, 6.7, 9.7, and 10.9 % for the full dataset, 1971, 1980, 1990, 2000 datasets respectively which is againg very close to the estimations of the model using OLS methodology. But the latter estimated far away coefficients for the provided samples of the data with initial values of 0.1 for all coefficients and tolerance level of 1e-15. However, after changing the initial values of the coefficients in the optimization method, I received the same estimations as the ones in OLS and other MLE optimization methods.
#
# **All in all, education and wages are positively correlated and increasing the years of education will lead to higher wages.**
