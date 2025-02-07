# -*- coding: utf-8 -*-
"""LOR-TechnicalAssessment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yLndQy2TI2dGgrHfHL_sQcEGtdVP6NtQ

#Data source: 

https://archive.ics.uci.edu/ml/datasets/Online+Retail

# Data Set Information:

This is a transnational data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.The company mainly sells unique all-occasion gifts. Many customers of the company are wholesalers.

# Attribute Information:

InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.
StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.
Description: Product (item) name. Nominal.
Quantity: The quantities of each product (item) per transaction. Numeric.
InvoiceDate: Invice Date and time. Numeric, the day and time when each transaction was generated.
UnitPrice: Unit price. Numeric, Product price per unit in sterling.
CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.
Country: Country name. Nominal, the name of the country where each customer resides.
"""

#Load libraries
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from google.colab import drive

#Import data
retail_data=pd.read_excel('https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx',index_col='InvoiceDate',parse_dates=True)

#Review import stats
retail_data.info()
retail_data.head()
retail_data.index[0]

"""Note that there are 1554 missing descriptions and 135080 missing CustomerIDs"""

#Provide OrderValue to see size of order
retail_data['OrderValue']=retail_data['Quantity']*retail_data['UnitPrice']
retail_data[['Quantity','UnitPrice','OrderValue']].describe()

#Visualise the data to ID gross error
retail_data[["Quantity","UnitPrice","OrderValue"]].plot(marker='.',alpha=0.5,figsize=(20,30),subplots=True)

#Check top 10 largest/smallest orders by quantity
retail_data.nlargest(10,"Quantity")

retail_data.nsmallest(10,"Quantity")

#assume normal distribution and filter to within 2std of the mean to cull outliers. 
std_ordervalue=retail_data[["OrderValue"]].std()
mean_ordervalue=retail_data[["OrderValue"]].mean()
upperboundary=mean_ordervalue+(2*std_ordervalue)
lowerboundary=mean_ordervalue-(2*std_ordervalue)
retail_data_nooutliers=retail_data[(retail_data["OrderValue"]>=-739.633)&(retail_data["OrderValue"]<=775.61)]
retail_data_nooutliers[["Quantity","UnitPrice","OrderValue"]].describe()

"""N.B the means have barely changed across quantity, unit price and order value => Not a bad assumption"""

#Visulise data set again
retail_data_nooutliers[["Quantity","UnitPrice","OrderValue"]].plot(figsize=(20,30),subplots=True)

#Resample to see weekly averages
retail_weekly=retail_data_nooutliers.resample("W").mean()
retail_weekly[["Quantity","UnitPrice","OrderValue"]].plot(figsize=(20,30),subplots=True)

"""#Analysis of Countries

```
# This is formatted as code
```
"""

#Add a column of 1 to provide groupby count
retail_data_nooutliers['no_transactions']=1
top_countries=retail_data_nooutliers.groupby(by="Country").sum().sort_values(by=["OrderValue"],ascending=False)
top_countries['pct_OrderValue']=top_countries.OrderValue/top_countries.OrderValue.sum()
top_countries

retail_UK=retail_data_nooutliers[retail_data_nooutliers.Country=="United Kingdom"]
retail_UK["OrderValue"].resample("W").sum().plot(figsize=(20,10))

ax=retail_UK["OrderValue"].resample("D").sum().rolling(window=28).mean().plot(figsize=(20,10),sharey='Daily Order Value (£)',title='United Kingdom Daily Order Value Rolling 28 Day Average')
ax.set_ylabel("Daily Order Value")

"""#Analysis of Customers"""

top_customers=retail_data_nooutliers.groupby(by="CustomerID").sum().sort_values(by=["OrderValue"],ascending=False)
top_customers['pct_OrderValue']=top_customers.OrderValue/top_customers.OrderValue.sum()
top_customers

#Check worst customer, check full data incase of outliers
retail_data[retail_data.CustomerID==14213]

"""The above customer has received 5no. refunds 3 days after start of data collection. Likely missing earlier transaction but check for fraud?"""

#check second worst customer, more transactions by no., check full data
retail_data[retail_data.CustomerID==17603]

"""These invoices were raised significantly after the start of the dataset, appears to have beeen given "manual" credit? Should be investigated"""