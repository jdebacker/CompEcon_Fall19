### CompEcon Fall'19 PS5: Devashish Thakar

# Part B: Econometric Estimation
# Installing and uploading important packages
install.packages("lmtest")
install.packages("sandwich")
install.packages("stargazer")
library(lmtest)
library(sandwich)
library(stargazer)

# Import the data:
df<-read.delim(file = "clipboard")

# Make Average Revenue per User Numeris
df$ARPU <- as.numeric(df$ARPU)

# Normalize Earnings before taxes to million
df$EBITDA<-df$EBITDA/1000000

# Create some dummy variables for treatment and time
df$After<-ifelse(df$Time.from.launch<0,0,1)

# Create a dummy variable if its a first launch or subsequent launch
df$launc_seq<-ifelse(df$Launch.Seq=='Only Launch'|
                       df$Launch.Seq=='First Launch',1,0)

# Dummy variable for launch experience to be used later:
df$launch_exp<-ifelse(df$Prior_Launch_Exp=='No Prior Exp',0,1)

# First Model to compare first launch vs subsequent launches
EBITDA1_OLS<-lm(df$EBITDA ~  After*launc_seq + Population + HHI + 
                as.factor(Market_Operator) + as.factor(Year),
                data = df )
# Summarizing the results
summary(EBITDA1_OLS)

# Second Model to compare the performance of 
# experienced vs inexperienced MNO's in first launches
EBITDA2_OLS<-lm(EBITDA ~  After*launch_exp + Population + HHI + 
                as.factor(Market_Operator)+ as.factor(Year),
                data = df[df$launc_seq==1,])

# Summarizing the results
summary(EBITDA2_OLS)

# Third Model to compare the performance of 
# experienced vs inexperienced MNO's in subsequent launches
EBITDA3_OLS<-lm(EBITDA ~  After*launch_exp + Population + HHI + 
                as.factor(Market_Operator)+ as.factor(Year),
                data = df[df$launc_seq==0,])

# Summarizing the results
summary(EBITDA3_OLS)

# Storing the output using stargazer
stargazer(EBITDA1_OLS,EBITDA2_OLS,EBITDA3_OLS, type="latex",
          dep.var.labels = c("EBITDA Overall","EBITDA First Launch",
                             "EBITDA Subsequent Launch"),
          omit = c("Market_Operator","Year"),digits = 3,
          omit.labels = c("MNO FE","Year FE") ,out="EBITDA_OLS.tex")
