#install.packages("MSwM")
#install.packages("msm")
#install.packages("xtable")
#install.packages("knitr")

library(MSwM)
library(msm)
library(readxl)
library(ggplot2)
library(tidyr)
library(dplyr)
library(knitr)
library(xtable)

setwd("C:/Users/PhD.Econ/Desktop/PS5")

ms_dcc <- read_excel("C:/Users/PhD.Econ/Desktop/PS5/ms-dcc.xlsx")
View(ms_dcc)

dataset1 <- ms_dcc %>%
         select(date, CORR, GR, IM, P, REER, POIL)
         gather(key = "variable", value = "value", -date)
         head(dataset1, 7)
dataset2 <- ms_dcc %>%
         select(date, CORR, GR, CAPITALG, CONSUMPTIONG, INTERMEDIATEG,
           P, REER, POIL)
         gather(key = "variable", value = "value", -date)
         head(dataset1, 9)
dfGraph <- ms_dcc %>%
         select(year, CAPITALG, CONSUMPTIONG, INTERMEDIATEG) %>%
         gather(key = "variable", value = "value", -year)
         head(dfGraph, 4)

plot(CORR~IM, data=ms_dcc,
     main ="Imports and Correlation of Variables of Interest",
     xlab ="IM (Total Imports of Iran)",
     ylab ="CORR (Dynamic Correlation)")
plot(CORR~INTERMEDIATEG, data=ms_dcc,
    main ="Intermediate Goods Import and the Dynamic Correlation",
    xlab ="INTERMEDIATEG (Imports of Intermediate Goods in 100 Million USD)",
    ylab ="CORR (Dynamic Correlation)")
ggplot(dfGraph, aes(x = year, y = value)) +
       geom_area(aes(color = variable, fill = variable),
                 alpha = 0.5, position = position_dodge(0.8)) +
       scale_color_manual(values = c("#00AFBB", "#E7B800", "#FC4E07")) +
       scale_fill_manual(values = c("#00AFBB", "#E7B800", "#FC4E07")) +
       labs(title = "Imports of Iran Separated by Type - 100 Million USD")

summary(dataset1)
summary(dataset2)
str(dataset1)
str(dataset2)

OLS1 <- lm(dataset1$CORR ~ dataset1$GR + dataset1$P + dataset1$REER +
           dataset1$POIL + dataset1$IM)
     OLS1
     summary(OLS1)
     coeftest(OLS1, vcov = vcovHC(OLS1, "HC1"))
     print(xtable(OLS1, type = "latex"), file = "OLS1.tex")
OLS2 <- lm(dataset2$CORR ~ dataset2$GR + dataset2$P + dataset2$REER +
           dataset2$POIL + dataset2$CAPITALG + dataset2$CONSUMPTIONG +
           dataset2$INTERMEDIATEG)
     OLS2
     summary(OLS2)
     coeftest(OLS2, vcov = vcovHC(OLS2, "HC1"))
     print(xtable(OLS2, type = "latex"), file = "OLS2.tex")

model1 = lm(dataset1$CORR ~ dataset1$GR + dataset1$P + dataset1$REER +
           dataset1$POIL + dataset1$IM)
model2 = lm(dataset2$CORR ~ dataset2$GR + dataset2$P + dataset2$REER +
           dataset2$POIL + dataset2$CAPITALG + dataset2$CONSUMPTIONG +
           dataset2$INTERMEDIATEG)

msm1 = msmFit(model1, k = 2, sw = rep(TRUE, 7))
summary(msm1)
#print(xtable(msm1, type = "latex"), file = "msm1.tex") # Does not support msmFit, ...
plotProb(msm1, which = 1)
plotReg(msm1)

msm2 = msmFit(model2, k = 2, sw = rep(TRUE, 9))
summary(msm2)
plotProb(msm2, which = 1)
plotReg(msm2)
