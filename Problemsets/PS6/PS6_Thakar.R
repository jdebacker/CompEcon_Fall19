### CompEcon Fall'19 PS6: Devashish Thakar

# Part B: Econometric Estimation
# Installing and uploading important packages
install.packages("lmtest")
install.packages("sandwich")
install.packages("stargazer")
install.packages("openxlsx")
install.packages('gmm')
install.packages("plm")
install.packages("lmtest")
library(lmtest)
library(sandwich)
library(stargazer)
library(openxlsx)
library(gmm)
library(plm)
library(lmtest)

# Import the data:
df<-read.xlsx( "C:/Users/Devashish/Desktop/CompEcon_Fall19/Problemsets/PS6/PS6_Data.xlsx",1)


# First Model to compare first launch vs subsequent launches
Price_OLS<-lm(price ~  dealer_rating + dealer_num_review
              + as.factor(year)+as.factor(vehicle_brand) 
              + num_convenience + num_safety + num_exterior
              + num_seating + num_entertainment,
                data = df )

summary(Price_OLS)

Price_RE<-plm(price ~  dealer_rating + dealer_num_review + as.factor(year)
              + num_convenience + num_safety + num_exterior
              + num_seating + num_entertainment, model="pooling",
              data = df, index=c("vehicle_brand"))
Price_RE1<-coeftest(Price_RE,vcov=vcovHC(Price_RE,type="HC0",cluster="group"))

summary(Price_RE)

# Summarizing the results
summary(Price_OLS)

# Storing the output using stargazer
stargazer(Price_OLS,Price_RE1, type="latex",
          dep.var.labels = c("Price"),
          omit = c("year","vehicle_brand"),digits = 3,
          omit.labels = c("Year FE","Brand FE") ,out="PS6_Results.tex")
