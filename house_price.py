#!/usr/bin/env python
import pandas as pd
import os
import math
import matplotlib.pyplot as plt

Price = None
price_min = 200000
price_max = 1500000
Currency = None
LocationCity = 'İstanbul'
LocationCounty = 'Sarıyer'
LocationDistrict = 'İstinye Mah.'
LocationLatitude = None
LocationLongitude = None
Date = None
Type = None
m2 = None
RoomCount = None
BuildingAge = None
Floor = None
TotalFloor = None
Heating = None
Bathrooms = None
Furnished = None
Status = None
Residential = None # Site icerisinde 
Dues = None # Aidat
AvailableforLoan = None # Kredi
SalerType = None
Exchange = None

def loadCSV(filepath):
	global df
	df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + filepath,encoding='utf-8',names=['title','id','price','currency','city','county','district','lat','lon','date','type','m2','room','age','floor','total_floor','heating','bathroom','furnished','status','residental','dues','loan','saler','exchange'])

def searchDF():
	global Price
	global price_min
	global price_max
	global LocationCity
	global LocationCounty
	global LocationDistrict
	global LocationLatitude
	global LocationLongitude
	global Type
	global m2
	global RoomCount
	global BuildingAge
	global Floor
	global TotalFloor
	global Heating
	global Bathrooms
	global Furnished
	global Status
	global Residential
	global Dues
	global AvailableforLoan
	global SalerType
	global Exchange

	global df
	global df_found

	df_found = df.loc[df['city'] == LocationCity]
	print('City: \t\t\t' + LocationCity + ' (' + str(len(df_found)) + ')')
	df_found = df_found.loc[df_found['county'] == LocationCounty]
	print('County: \t\t' + LocationCounty + ' (' + str(len(df_found)) + ')')
	df_found = df_found.loc[df_found['district'] == LocationDistrict]
	print('District: \t\t' + LocationDistrict + ' (' + str(len(df_found)) + ')')
	df_found = df_found[(df_found['price'] >= price_min) & (df_found['price'] <= price_max)]
	print('Price Range: \t' + str(price_min) + '-' + str(price_max) + ' (' + str(len(df_found)) + ')')

def doMath():
	global df_found
	prices_2 = []
	total_price = 0
	for x in df_found.price:
		prices_2.append(x)
		total_price = total_price + x
	print('Average Price: \t' + str(int(total_price / len(prices_2))))

def plotGraph():
	global df
	global prices
	prices = []

	for x in df.price:
		prices.append(int(x))

	# Make prices in order
	prices.sort()

	#plt.plot(prices)
	plt.ylabel('Prices')
	plt.xlabel('Count')
	plt.plot(range(0, len(prices)),prices)

	#plt.axis([0, len(prices), 0, max(prices)])
	#plt.axis([0, len(prices), 0, max(prices)])

	#plt.savefig('test.png')
	plt.show()

if __name__ == '__main__':
	loadCSV('/inc/real_estate_data.csv')
	searchDF()
	doMath()
	#plotGraph()



