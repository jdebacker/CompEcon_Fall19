### ComEcon Fall'19 PS6 (Devashish Thakar)


# import packages
import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib
from tastypie import http
import http.client
from pandas import Series, DataFrame
import time
import matplotlib.pyplot as plt


# Code to extract key features from the listings on cars.com

'''
Defining a dictionary that will store the relevant details from each listing,
such as vehicle id, price, dealer ratings, car color etc.
'''

listing_dict={'vehicle_id':[],'listing_name':[],'vehicle_brand':[],
              'price':[],'dealer_name':[],'dealer_state':[],
              'dealer_rating':[],'dealer_num_review':[],'car_color':[],
              'dealer_url':[]}
'''
Defining a for loop to iterate over the first 50 pages of available listings
'''

for i in range(1,51):
    '''
    The general URL format only includes changing the page number.
    The filtering criteria used is nearest car listings for zip 
    code 29201.
    
    The try-except combination below ensures that the server transfer
    continues if the expected file size limit is breached. This is also 
    known as handling 'IncompleteRead' exceptions
    
    '''
    header = {'User-Agent': 'Mozilla/6.0'}
    URL=("https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&page="+str(i)+
         "&perPage=100&rd=99999&searchSource=GN_BREADCRUMB&sort=distance-nearest&zc=29201")
    try:
        oururl= urllib.request.urlopen(URL).read()
    except (http.client.IncompleteRead) as e:
        page = e.partial
    soup = BeautifulSoup(oururl)
    
    '''
    Details of each listing are stored in a json format. 
    temp_list extracts these details for each page. 
    
    Details of each listing are located in seperate json type structures. 
    The length of the temp_list file, threfore provides the number 
    of listings on each page
    '''
    
    temp_list=json.loads(soup.find("script",{"type":"application/ld+json","id":""}).text)
    length=len(temp_list)
    
    '''
    We then iterate over all the listings on a given page 
    and store the relevant listing details in the 
    dictionary created outside of the loop
    
    For some features such as dealer rating and number of review, 
    I had to add error handling because some of the dealers do not have ratings
    available and this causes the code to stop
    '''
    
    for j in range(0,len(temp_list)):
                listing_dict['vehicle_id'].append(temp_list[j]
                                          ['vehicleIdentificationNumber'])
        listing_dict['listing_name'].append(temp_list[j]
                                            ['name'])
        listing_dict['vehicle_brand'].append(temp_list[j]
                                             ['brand']['name'])
        listing_dict['price'].append(temp_list[j]
                                     ['offers']['price'])
        listing_dict['dealer_name'].append(temp_list[j]['offers']
                                           ['seller']['name'])
        listing_dict['dealer_state'].append(temp_list[j]['offers']['seller']
                                            ['address']['addressRegion'])
        try:
            listing_dict['dealer_rating'].\
            append(temp_list[j]
                   ['offers']['seller']['aggregateRating']['ratingValue'])
        except KeyError:
            listing_dict['dealer_rating'].append("")
        try:
            listing_dict['dealer_num_review'].\
            append(temp_list[j]
                   ['offers']['seller']['aggregateRating']['reviewCount'])
        except KeyError:
            listing_dict['dealer_num_review'].append("")
        listing_dict['car_color'].append(temp_list[j]['color'])
        listing_dict['dealer_url'].append(temp_list[j]['url'])    
    
    print('Page:',i)

    
# I convert the dictionary into a dataframe, with columns as the dictionary
# key, and the values as the dictionary value
df_listings=pd.DataFrame(dict([(k,Series(v)) for k,v in listing_dict.items()]))

# Extracting detailed features from each of the listings (~5000)
# The above code also provides me with dealer_url for ~5000 listings
# In the subsequent code, I access these dealer urls to extract
# detailed car features

# I need to iterate over the entire length of the listings_df
# Hence, I extract the length of the same
length1=listings_df.shape[0]+1

'''
Create an empty list to store list of features under each feature category
'''
listing_features=[]

for i in range(length1):
    '''
    Extract the URL from each listing to feed into Beautifulsoup
    '''
    
    URL =listings_df['dealer_url'][i]
    header = {'User-Agent': 'Mozilla/6.0'}
    try:
        oururl= urllib.request.urlopen(URL).read()
    except (http.client.IncompleteRead) as e:
        page = e.partial
    soup = BeautifulSoup(oururl)
    
    '''
    The data structure for the detailed listing is slightly complicated.
    There are 3-6 categories for detailed feature:
    1. Safety
    2. Entertainment
    3. Safety
    4. Exterior
    5. Seating
    
    I therefore store the result from each listing as a dictionary, with
    the key being one of the broad feature categories as above, and the 
    values being each feature within the category
    
    Therefore, I initialize a result dictionary at the beginning of each 
    iteration of the loop, to store the contents from features
    
    The detailed features for each listing are nested within a parent 
    class called: details-features-list--normalized-features, 
    which is extracted from the URL
    
    -->It contains several children classes, called "cui-heading-2", 
    which store the five broad feature categories defined above. 
    This becomes the 'Key'
    
    --> Each childrent class also has its own childrent class, called 
    "details-feature-list__item", which is the actual feature. These become
    the 'value'. Since there are multiple values within each 'Key', 
    we iterate over all of them
    
    '''
    
    result = {}
    for group in soup.find_all("div",
                               {"class": "details-feature-list--normalized-features"}):
        result[group.find("h2", 
                          {"class": "cui-heading-2"}).text] =\
    [itm.text for itm in group.find_all("li",
                                        {"class": "details-feature-list__item"})]
    listing_features.append(result)

# We create a dataframe of all the features. The categories become the 
# columns, while the values remains values for each observation
df_features=pd.DataFrame(listing_features)

# Combine the listings with their features:
df=pd.concat([df_listings, df_features],axis=1).replace(np.nan, '', regex=True)

# Aggregating price by brand
df['price']=pd.to_numeric(df['price'])
df_brand=df.groupby(['vehicle_brand']).agg({'price':'mean'}).reset_index().\sort_values('price')

# Plotting brand vs average price
plt.style.use('ggplot')
fig, ax = plt.subplots() # make figure and axes separate objects
plt.bar(df_brand['vehicle_brand'], df_brand['price'],
        align='center',alpha=.5, width=0.5)
plt.xticks(df_brand['vehicle_brand'])

# Rotating x-axis labels to make them visible
plt.xticks(rotation=90)
plt.ylabel('Average Price')
plt.xlabel('Brand')
plt.title('Average Price by Brand')
fig.savefig('Price_by_brand.jpg', transparent=False,
            dpi=80, bbox_inches="tight")


# It seems like Lamborghini and Rolls Royce are the obvious outliers.
# I leave those two out and redo the plot

df_brand1=df_brand[~df_brand.vehicle_brand.isin(['Lamborghini','Rolls-Royce'])]

# Plotting brand vs average price
plt.style.use('ggplot')
fig, ax = plt.subplots() # make figure and axes separate objects
plt.bar(df_brand1['vehicle_brand'], df_brand1['price'], 
        align='center',alpha=.5, width=0.5)
plt.xticks(df_brand1['vehicle_brand'])

# Rotating x-axis labels to make them visible
plt.xticks(rotation=90)
plt.ylabel('Average Price')
plt.xlabel('Brand')
plt.title('Average Price by Brand')
fig.savefig('Price_by_brand1.jpg', 
            transparent=False, dpi=80, bbox_inches="tight")

# This is kind of expected, with luxury brands such as Bentley, Tesla, MB etc.,
# having the highest prices

# But I aim to understand the prices vs. features relationship
# Are the prices for used cars higher for more exterior or for more convenience 
# fetures, and so on....

# I add the number of features for Safety, Entertainment, Convenience, 
# Exterior & Seating. Each of the elements in this column is a list of
# features and I extract their number

num_convenience=[]
num_entertainment=[]
num_safety=[]
num_exterior=[]
num_seating=[]

# Iterate over all rows of the dataframe to calculate the number of features
# For loop was required becasue of the exception handling done within
for i in range (df.shape[0]):
    
    if len(df['Convenience'][i])==0:
        num_convenience.append(0)
    else:
        num_convenience.append(len(df['Convenience'][i].split(",")))
        
    if len(df['Safety'][i])==0:
        num_safety.append(0)
    else:
        num_safety.append(len(df['Safety'][i].split(",")))

    if len(df['Exterior'][i])==0:
        num_exterior.append(0)
    else:
        num_exterior.append(len(df['Exterior'][i].split(",")))

    if len(df['Seating'][i])==0:
        num_seating.append(0)
    else:
        num_seating.append(len(df['Seating'][i].split(",")))

    if len(df['Entertainment'][i])==0:
        num_entertainment.append(0)
    else:
        num_entertainment.append(len(df['Entertainment'][i].split(",")))

# Creating new columns for the number of features
df['num_safety']=num_safety
df['num_entertainment']=num_entertainment
df['num_exterior']=num_exterior
df['num_seating']=num_seating
df['num_convenience']=num_convenience

# Write out the new file to do econometric analysis in R
df.to_excel('PS6_Data.xlsx')

'''
The maximum number of 
conveience features=7
Safety features=7
Entertainment features=4
Exterior features=4
'''

# I look at the average price by convenience features:
df_convenience=df.groupby(['num_convenience']).\agg({'price':'mean'}).reset_index()
df_safety=df.groupby(['num_safety']).agg({'price':'mean'}).reset_index()
df_entertainment=df.groupby(['num_entertainment']).agg({'price':'mean'}).reset_index()
df_exterior=df.groupby(['num_exterior']).agg({'price':'mean'}).reset_index()
df_seating=df.groupby(['num_seating']).agg({'price':'mean'}).reset_index()


# Plotting average price versus number of features
df['price']=pd.to_numeric(df['price'])
df['num_convenience']=pd.to_numeric(df['num_convenience'])

# Setting up plot styles
plt.style.use('fivethirtyeight') # select a style (theme) for plot
fig, ax = plt.subplots() # make figure and axes separate objects
ax.set_xlim([0, 7]) # set axis range
ax.set_ylim([20000, 80000]) # set axis range


# Using line plots with num of features on x and price on y
plt.plot(df_convenience['num_convenience'], df_convenience['price'], 
         label='Convenience')
plt.plot(df_safety['num_safety'], df_safety['price'], label='Safety')
plt.plot(df_entertainment['num_entertainment'], 
         df_entertainment['price'],label='Entertainment' )
plt.plot(df_exterior['num_exterior'], df_exterior['price'], label='Exterior')
plt.plot(df_seating['num_seating'], df_seating['price'], label='Seating')

# Adding finishing touches to the plot
plt.legend()
ax.set(title='Avg. Price vs # of Features', xlabel='# of Features',
       ylabel="Avg. Price") # plot title, axis labels
fig.savefig('Price_by_features.jpg', 
            transparent=False, dpi=80, bbox_inches="tight")





