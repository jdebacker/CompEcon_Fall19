### ComEcon Fall'19 PS5 (Devashish Thakar)

#Part A:
#I am interested in understanding whether mobile network operators (MNO) 
#starting value-added services such as mobile payment services benefit 
#post-launch of these services
# First of all, I look at the launch of services and do some exploratory 
#data analysis with the service launch data

# Uploading the service launch dataset:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import squarify
df_service=pd.read_excel('Services_Info.xlsx')

####Figure 1: Number of value added services launched every year####

# Each row represents one value-added service
# Each column is the detail of that value added service
# Lets look at the distribution of services launched by year:
# I will use a bar plot to look at the frequency of launches by the year:

# Count of observations by launch year
df_launches=pd.DataFrame(df_service.groupby(['Launch_Year']).size().
                         reset_index(name='Num_of_Launches'))

# Details of plot features
plt.style.use('ggplot')
fig, ax = plt.subplots() # make figure and axes separate objects

# Actual plot command
plt.bar(df_launches['Launch_Year'], df_launches['Num_of_Launches'], 
        align='center',alpha=.5, width=0.8)
plt.xticks(df_launches['Launch_Year'])

# Sprucing up the plot and saving
plt.xticks(rotation=90)
plt.ylabel('Number of Launches')
plt.xlabel('Year')
plt.title('Launches by Year')
fig.savefig('Launch.jpg', transparent=False, dpi=80, bbox_inches="tight")


####Figure 2: Performance of mobile network operators post launch####

# The more interesting questions are how does the mobile network operator 
#(MNO) performance is affected post launch
# I combine the services launch dataset with a proprietary dataset with
#quarterly performance for many of the MNO and use this dataset for some more
# visualizations and econometric models

# Performance+Services information dataset
# It is a quarterly panel dataset of different MNO's with their 
#performance indices

# Loading the performance+service combined dataset
df_combined=pd.read_excel('Compiled Dataset.xlsx')

# Normalizing the Earnings before taxes (EBITDA) to million
df_combined['EBITDA']=df_combined['EBITDA']/1000000


#The above is a panel dataset of MNO performance over the a wide range 
#of years (2000-2014)
#Most of the launches happened in this time period, hence it allows us to 
#consider differences in pre and post performance launch

# Consider a subset of the dataset for MNO's that launched a service 
# and positive EBITDA (Earnings before income and taxes):
df_MNO=df_combined[(df_combined['Launched Mobile Money Services?']=='Laucnhed') 
                   & (df_combined['EBITDA']>=0)] 

# Creating an aggregate database to analyze the relationship 
# between EBITDA and ARPU (Avg. revenue per user) for scatter
df_MNO_analysis=df_MNO.groupby(['Launch Seq','Time from launch'])\
                  .agg({"EBITDA":"mean","ARPU":"mean"}).reset_index()


# Plotting the average EBITDA vs. ARPU for all the time sequences

# Setting plot chatacteristics
plt.style.use('fivethirtyeight') # select a style (theme) for plot
fig, ax = plt.subplots() # make figure and axes separate objects
ax.set_xlim([0, 50]) # set axis range
ax.set_ylim([0, 600]) # set axis range
# Scatter plot for EBITDA vs ARPU for post launch (Time from launch>=0)
plt.scatter(df_MNO_analysis[df_MNO_analysis['Time from launch']>=0]['ARPU'],
            df_MNO_analysis[df_MNO_analysis['Time from launch']>=0]['EBITDA'],
            c='b', label='Post-Launch' )
# Scatter plot for EBITDA vs ARPU for pre launch (Time from launch<0)
plt.scatter(df_MNO_analysis[df_MNO_analysis['Time from launch']<0]['ARPU'],
            df_MNO_analysis[df_MNO_analysis['Time from launch']<0]['EBITDA'],
            c='r',label='Pre-Launch' )
plt.legend()

# Sprucing up the plot and saving
ax.set(title='Avg. EBITDA vs. ARPU each quarter', xlabel='ARPU',
       ylabel="Avg EBITDA in mil $") # plot title, axis labels
fig.savefig('EBITDA-ARPU.jpg', transparent=False, dpi=80, bbox_inches="tight")


# From the above figure, it is clear that MNO's are able to improve their 
# earnings post launch without adding too much on the revenue side.
# Next,I look at the differences in EBITDA for first launcher and follower MNOs
# First Launchers are those MNO's that introduced such a service for the first
# time in this market
# Follower MNOs are those that did not make a first launch

#### Figure 3: Performance by launch sequence ####


plt.style.use('fivethirtyeight') # select a style (theme) for plot
fig, ax = plt.subplots() # make figure and axes separate objects
ax.set_xlim([-10, 10]) # set axis range
ax.set_ylim([0, 200]) # set axis range

# Plot performance for first launch
plt.plot(df_MNO_analysis[df_MNO_analysis['Launch Seq']==\
                         'First Launch']['Time from launch'],
         df_MNO_analysis[df_MNO_analysis['Launch Seq']==\
                         'First Launch']['EBITDA'],
         label='First Launch')
# Plot performance for subsequent launch
plt.plot(df_MNO_analysis[df_MNO_analysis['Launch Seq']==\
                         'Not first launch']['Time from launch'],
         df_MNO_analysis[df_MNO_analysis['Launch Seq']==\
                         'Not first launch']['EBITDA'],
         label='Non-first Launch')
ax.axvline(x=0, color='k', linestyle='--')
ax.set(title='Performance for First vs. Subsequent Launches', 
       xlabel='Quarter from launch',
       ylabel="Avg EBITDA in mil $") # plot title, axis labels
leg = ax.legend();
fig.savefig('Launch-Seq.jpg', transparent=False, dpi=80, bbox_inches="tight")


# From the above, it can be seen that follower MNO's outperform the first 
# launcher MNOs post launch. 
# The next question I want to explore is whether this difference is 
# enhanced for MNO's that had the experience of launching such services 
# in other markets (Prior Experience=1)
# I also split my sample into first launches and subsequent launches 
# to see the differential impact of prior experience by launch sequence
# But is there a difference for MNO's with prior launch experience
# in other markets?

# Creating an agggreated database for first launches and subsequent launches
df_MNO_FirstLaunch=df_MNO[df_MNO['Launch Seq']=='First Launch']\
                   .groupby(['Prior_Launch_Exp','Time from launch'])\
                   .agg({"EBITDA":"mean"}).reset_index()
df_MNO_SubsequentLaunch=df_MNO[df_MNO['Launch Seq']=='Not first launch']\
                   .groupby(['Prior_Launch_Exp','Time from launch'])\
                   .agg({"EBITDA":"mean"}).reset_index()

### Fig 4: Performance for first launch by prior launch experience###

# Performance for first launches
plt.style.use('fivethirtyeight') # select a style (theme) for plot
fig, ax = plt.subplots() # make figure and axes separate objects
ax.set_xlim([-10, 10]) # set axis range
ax.set_ylim([0, 200]) # set axis range

# With prior experience
plt.plot(df_MNO_FirstLaunch[df_MNO_FirstLaunch['Prior_Launch_Exp']==
                            'Prior Exp']['Time from launch'],
         df_MNO_FirstLaunch[df_MNO_FirstLaunch['Prior_Launch_Exp']==
                            'Prior Exp']['EBITDA'], label='Exp.MNO')
# Without prior experience
plt.plot(df_MNO_FirstLaunch[df_MNO_FirstLaunch['Prior_Launch_Exp']==
                            'No Prior Exp']['Time from launch'],
         df_MNO_FirstLaunch[df_MNO_FirstLaunch['Prior_Launch_Exp']==
                            'No Prior Exp']['EBITDA'], label='Non-Exp. MNO')

# Tidying up the plot a little
ax.axvline(x=0, color='k', linestyle='--') # plot the launch line indicator
ax.set(title='Performance for First launches',
       xlabel='Quarter from launch',
       ylabel="Avg EBITDA in mil $") # plot title, axis labels
leg = ax.legend();

# Saving the plot
fig.savefig('First-Launch-Experience.jpg', transparent=False, 
            dpi=80, bbox_inches="tight")


# From the above, it seems that for first of its kind launches in a market, 
# MNO's with prior service experience in other markets fare poorly
# Next I look at the performance by expereince by subsequent launches

### Fig 5: Performance for subsequent launches by prior launch experience ###

# Performance for first launches
plt.style.use('fivethirtyeight') # select a style (theme) for plot
fig, ax = plt.subplots() # make figure and axes separate objects
ax.set_xlim([-10, 10]) # set axis range
ax.set_ylim([0, 200]) # set axis range

# With prior experience
plt.plot(df_MNO_SubsequentLaunch[df_MNO_SubsequentLaunch['Prior_Launch_Exp']==
                                 'Prior Exp']['Time from launch'],
         df_MNO_SubsequentLaunch[df_MNO_SubsequentLaunch['Prior_Launch_Exp']==
                                 'Prior Exp']['EBITDA'],
         label='Exp.MNO')

# Without prior experience
plt.plot(df_MNO_SubsequentLaunch[df_MNO_SubsequentLaunch['Prior_Launch_Exp']==
                                 'No Prior Exp']['Time from launch'],
         df_MNO_SubsequentLaunch[df_MNO_SubsequentLaunch['Prior_Launch_Exp']==
                                 'No Prior Exp']['EBITDA'],
         label='Non-Exp. MNO')

# Tidying up the plot a little
ax.axvline(x=0, color='k', linestyle='--')
ax.set(title='Performance for subsequent launches',
       xlabel='Quarter from launch',
       ylabel="Avg EBITDA in mil $") # plot title, axis labels
leg = ax.legend();

# Saving the plot
fig.savefig('Non-first-Launch-Experience.jpg', transparent=False, 
            dpi=80, bbox_inches="tight")


# From the above, for subsequent launches, MNO's with prior launch experience 
# outperform inexperienced MNO's

##### End of Code #####