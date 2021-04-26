## ===============================================================================================================
## EXPLORATORY DATA ANALYTICS
## ===============================================================================================================

setwd("D:/OneDrive - Nanyang Technological University/DIGIPEN_TFIP_IBF_LESSONS/Week 8 - Day 5")

## Read Input data
sales = read.csv("sales.csv", header = TRUE)

## Explore Structure and Summary of Input data
str(sales)
summary(sales)

## OBSERVATIONS:
##  1.  Dependent Variable:  Store_Sales
##  2.  All independent variables are numeric or integer expect Parking and Coupon_Category
##  3.  Missing values present in Dist_Taxi, Dist_Market, Dist_Metro, Store_Area and Items_Available
##  4.  Max value for Store_Sales is very high compared to 3rd Qu - Possibility of outliers?
##  5.  Similar outlier possibility found in Store_Area, Items_Available, Dist_Metro and Dist_Market

## *************************
##  Examine Dependent Variable Store_Sales

attach(sales)

##  Build Histogram for Store_Sales to understand its distribution
hist(Store_Sales)

##  OBSERVATIONS:
##  Most of the Sales are at the lower end thus skewing the histogram - further strengthens possibility of outliers

##  For now, let us examine only the mid to low Store_Sales (< 500000)

Store_Sales_low = Store_Sales[Store_Sales < 500000]

hist(Store_Sales_low)

##  OBSERVATIONS:
##  Number of obs reduced from 897 to 896 - Therefore, there was only 1 obs that had Store_Sales > 500000
##  Store_Sales resembles Normal Distribution


##  Let us now examine the Numeric Independent variables using the original Sales dataset
names(sales)

hist(Dist_Taxi)

hist(Dist_Market)

hist(Dist_Metro)

hist(Store_Area)      ## Looks Right Skewed - Needs closer examination
boxplot(Store_Area)   ## Seems like one Store is very large compared to others - Outlier again?

hist(Items_Available)       ## Looks Right Skewed 
boxplot(Items_Available)    ## Seems like one Store has large number of items - Maybe company Mega Store?

hist(Daily_Customer_Count)

## Now let us examine the Categorical Variables

table(Parking)
plot(as.factor(Parking))

table(Coupon_Category)
plot(as.factor(Coupon_Category))

## *************************
##  MISSING VALUES TREATMENT
## *************************

##  Options Available:
##    1.  Remove records having missing values
##    2.  Impute values

##  To start, let us remove records with missing values
sales_complete = sales[complete.cases(sales),]
nums <- unlist(lapply(sales_complete, is.numeric))  
boxplot(sales_complete[,nums] , col = "green", main = "Box Plot for Store Sales")


##  Hard to read the plot - One high Store_Sales value hurting the scale
##  Let us replot without this high sales store
sales_complete_2 = subset(sales_complete, sales_complete$Store_Sales < 500000)
boxplot(sales_complete_2[,nums])

attach(sales_complete_2)

plot(sales_complete_2[,c(2:6, 9:10)])    ## Excluded Observation and Categorical variables
cor(sales_complete_2[,c(2:6, 9:10)])

##  OBSERVATIONS:
##  1.  Store_Area and Items_Available are very highly correlated - Almost perfect positive correlation
##  2.  Dist_Taxi and Dist_Metro are also highly correlated
##  3.  Dist_Market and Dist_Metro are fairly well correlated
##  4.  Dependent variable Store_Sales does not have a strong correlation with any independent variable
##        So which independent variables have the greatest influence on Store_Sales?

boxplot(sales_complete_2[,c(2:6,9:10)], col = "orange", main = "Box Plot for Store Sales")

##  OBSERVATIONS:
##  The high values of Store_Sales is making it hard to interpret the box plot - Let us try scaling the variables

boxplot(scale(sales_complete_2[,c(2:6,9:10)]), col = "orange")
##  OBSERVATIONS:
##  Much better distribution for all variables


## Examine Categorical Variables and their relationship with Store_Sales

names(sales_complete_2)
boxplot(Store_Sales ~ Coupon_Category,
        xlab= "Coupon_Category",ylab="Store Sales",
        main="Store Sales by Coupon Category",col=c("Orange","blue","grey"))

##  OBSERVATIONS:
##  Coupon_Category has a significant impact on Store_Sales

boxplot(Store_Sales ~ Parking,
        xlab= "Parking",ylab="Store Sales",
        main="Store Sales by Parking",col=c("Red", "Orange","blue","grey"))

##  OBSERVATIONS:
##  Parking does not seem to have a significant impact on Store_Sales


##  Now, let us try to impute missing values

library(mice)
library(VIM)

## First let us understand the missing values pattern using the function md.pattern
md.pattern(sales)
help(md.pattern)
##  OBSERVATIONS:
##  1.  There are 898 obs which has zero missing values
##  2.  There are 7 obs for which Store_Area values are missing
##  3.  There are 14 obs for which Items_Available values are missing
##  4.  There are 12 obs for which Dist_Taxi and Dist_Market values are missing
##  5.  There is 1 obs for which Dist_Metro, Store_Area, Dist_Taxi, Dist_Market and Items_Available values are missing

## Let us plot the above information
sales_miss = aggr(sales, col=mdc(1:3), numbers=TRUE, sortVars=TRUE,
                  labels=names(sales), cex.axis=.7, gap=3,
                  ylab=c("Proportion of missingness","Missingness Pattern"))

#help(aggr)
## IMPUTING MISSING VALUES USING mice PACKAGE
## If any variable contains missing values, the mice package regresses it over the other variables and 
## predicts the missing values. Some of the available models in mice package are:
##    PMM (Predictive Mean Matching) - suitable for numeric variables
##    logreg(Logistic Regression) - suitable for categorical variables with 2 levels
##    polyreg(Bayesian polytomous regression) - suitable for categorical variables with more than or equal to two levels
##    Proportional odds model - suitable for ordered categorical variables with more than or equal to two levels

mice_imputes = mice(sales, m = 5, maxit = 7)   ## m: Number of times model should run, maxit: Max number of iterations

names(mice_imputes)

## Methods mice used for imputing
mice_imputes$method

##    Since only numeric variables had missing values, mice used pmm method 

## Now let us first examine the values mice determined for Dist_Taxi
mice_imputes$imp$Dist_Taxi

## Before inserting the values, let us look at rows 50, 161 and 207 - They all have missing values
sales[c(50,161,207),]

## Impute Data
imputed_data = complete(mice_imputes, 5)

## Let us look at the same rows 50, 161 and 207
imputed_data[c(50,161,207),]

## Has the imputed value changed the Descriptive Statistics?
summary(sales$Dist_Taxi)
summary(imputed_data$Dist_Taxi)

summary(sales$Dist_Market)
summary(imputed_data$Dist_Market)

summary(sales$Store_Area)
summary(imputed_data$Store_Area)

summary(sales$Items_Available)
summary(imputed_data$Items_Available)

## Create Density plot - Each red line represents an imputed value, should be similar to the blue line
densityplot(mice_imputes)

## OBSERVATIONS:
##  1.  mice has found values that do not significantly alter the Descriptive Statistics of fields with missing values

detach(sales)

## ****************************************************************************************************
##  CONCLUSIONS:
## ****************************************************************************************************

##  1.  The store sales dataset had both outliers and missing values that needed to be addressed
##  2.  There was one outlier in Store_Sales which significantly altered the distribution.  Domain knowledge is required
##      to make a decision about this store.  It is possible that this is a Mega Signature Store or just a typing error.
##  3.  Imputing missing values required us to use the mice package.  Seems like the outcome did not significantly alter the
##      Descriptive Statistics. 
##  4.  DATA IS NOW READY FOR MODEL BUILDING!!!
