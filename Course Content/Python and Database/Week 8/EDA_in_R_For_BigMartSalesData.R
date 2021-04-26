#Big Mart Sales: EDA 
#Problem Statement
#The data scientists at BigMart have collected 2013 sales data for 1559 products across 
#10 stores in different cities. 
#Also, certain attributes of each product and store have been defined. 

#Hypothesis Generation

#We'll first load the required packages.
library(data.table)
library(dplyr)
library(ggplot2)
library(caret)
library(corrplot)
library(e1071)
library(cowplot)

# Load the data 
data = read.csv("BigMartSalesData.csv")

# Check the diamention of the dataset
dim(data)

# Feature names dataset
names(data)

# Structure of the dataset
str(data)

#check missing values
table(is.na(data))
      
#check the train data which values are missing
colSums(is.na(data))

#Descriptive statistics
summary(data)

#Exploratory Data Analysis
#Univariate Analysis
##Since our target variable is continuous, we can visualise it by plotting its histogram.
ggplot(data) + geom_histogram(aes(data$Item_Outlet_Sales), binwidth = 100, fill = "darkgreen") +
  xlab("Item_Outlet_Sales")

#Independent Variables (numeric variables)
##Now let's check the numeric independent variables. We'll again use the histograms for visualizations because that will help us in visualizing the distribution of individual variables.
p1 = ggplot(data) + geom_histogram(aes(Item_Weight), binwidth = 0.5, fill = "blue")
p2 = ggplot(data) + geom_histogram(aes(Item_Visibility), binwidth = 0.005, fill = "blue")
p3 = ggplot(data) + geom_histogram(aes(Item_MRP), binwidth = 1, fill = "blue")
plot_grid(p1, p2, p3, nrow = 1) # plot_grid() from cowplot package

#Independent Variables (categorical variables)
ggplot(data %>% group_by(Item_Fat_Content) %>% summarise(Count = n())) + 
  geom_bar(aes(Item_Fat_Content, Count), stat = "identity", fill = "coral1")

#In the figure above, 'LF', 'low fat', and 'Low Fat' are the same category and 
#can be combined into one. Similarly we can be done for 'reg' and 'Regular' 
#into one. After making these corrections we'll plot the same figure again.

data$Item_Fat_Content[data$Item_Fat_Content == "LF"] = "Low Fat"
data$Item_Fat_Content[data$Item_Fat_Content == "low fat"] = "Low Fat"
data$Item_Fat_Content[data$Item_Fat_Content == "reg"] = "Regular"
ggplot(data %>% group_by(Item_Fat_Content) %>% summarise(Count = n())) + 
  geom_bar(aes(Item_Fat_Content, Count), stat = "identity", fill = "coral1")


p4 = ggplot(data %>% group_by(Item_Type) %>% summarise(Count = n())) + 
  geom_bar(aes(Item_Type, Count), stat = "identity", fill = "coral1") +
  xlab("") +
  geom_label(aes(Item_Type, Count, label = Count), vjust = 0.5) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))+
  ggtitle("Item_Type")
p5 = ggplot(data %>% group_by(Outlet_Identifier) %>% summarise(Count = n())) + 
  geom_bar(aes(Outlet_Identifier, Count), stat = "identity", fill = "coral1") +
  geom_label(aes(Outlet_Identifier, Count, label = Count), vjust = 0.5) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
p6 = ggplot(data %>% group_by(Outlet_Size) %>% summarise(Count = n())) + 
  geom_bar(aes(Outlet_Size, Count), stat = "identity", fill = "coral1") +
  geom_label(aes(Outlet_Size, Count, label = Count), vjust = 0.5) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
second_row = plot_grid(p5, p6, nrow = 1)
plot_grid(p4, second_row, ncol = 1)

p7 = ggplot(data %>% group_by(Outlet_Establishment_Year) %>% summarise(Count = n())) + 
  geom_bar(aes(factor(Outlet_Establishment_Year), Count), stat = "identity", fill = "coral1") +
  geom_label(aes(factor(Outlet_Establishment_Year), Count, label = Count), vjust = 0.5) +
  xlab("Outlet_Establishment_Year") +
  theme(axis.text.x = element_text(size = 8.5))
p8 = ggplot(data %>% group_by(Outlet_Type) %>% summarise(Count = n())) + 
  geom_bar(aes(Outlet_Type, Count), stat = "identity", fill = "coral1") +
  geom_label(aes(factor(Outlet_Type), Count, label = Count), vjust = 0.5) +
  theme(axis.text.x = element_text(size = 8.5))
plot_grid(p7, p8, ncol = 2)


#Bivariate Analysis
##After looking at every feature individually, let's now explore them again 
#with respect to the target variable. Here we will make use of scatter plots 
#for continuous or numeric variables and violin plots for the categorical variables.
p9 = ggplot(data) + geom_point(aes(Item_Weight, Item_Outlet_Sales), colour = "violet", alpha = 0.3) +
  theme(axis.title = element_text(size = 8.5))
p10 = ggplot(data) + geom_point(aes(Item_Visibility, Item_Outlet_Sales), colour = "violet", alpha = 0.3) +
  theme(axis.title = element_text(size = 8.5))
p11 = ggplot(data) + geom_point(aes(Item_MRP, Item_Outlet_Sales), colour = "violet", alpha = 0.3) +
  theme(axis.title = element_text(size = 8.5))
second_row_2 = plot_grid(p10, p11, ncol = 2)
plot_grid(p9, second_row_2, nrow = 2)

p12 = ggplot(data) + geom_violin(aes(Item_Type, Item_Outlet_Sales), fill = "magenta") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.text = element_text(size = 6),
        axis.title = element_text(size = 8.5))
p13 = ggplot(data) + geom_violin(aes(Item_Fat_Content, Item_Outlet_Sales), fill = "magenta") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.text = element_text(size = 8),
        axis.title = element_text(size = 8.5))
p14 = ggplot(data) + geom_violin(aes(Outlet_Identifier, Item_Outlet_Sales), fill = "magenta") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        axis.text = element_text(size = 8),
        axis.title = element_text(size = 8.5))
second_row_3 = plot_grid(p13, p14, ncol = 2)
plot_grid(p12, second_row_3, ncol = 1)

ggplot(data) + geom_violin(aes(Outlet_Size, Item_Outlet_Sales), fill = "magenta")

#Missing Value Treatment
colSums(is.na(data))
missing_index = which(is.na(data$Item_Weight))
for(i in missing_index){
  
  item = data$Item_Identifier[i]
  data$Item_Weight[i] = mean(data$Item_Weight[data$Item_Identifier == item], na.rm = T)
  
}

#Replacing 0's in Item_Visibility variable
zero_index = which(data$Item_Visibility == 0)
for(i in zero_index){
  
  item = data$Item_Identifier[i]
  data$Item_Visibility[i] = mean(data$Item_Visibility[data$Item_Identifier == item], na.rm = T)
  
}


