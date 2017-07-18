#!usr/bin/python

import pandas as pd
import re

parkingData = pd.read_csv('./parking2007_2008.csv')

parkingData.dropna(how='all', inplace=True)

streetPattern = re.compile('[A-Z0-9]+(?=\sAVE|\sST)')

def locationToAddress(location):
	location = str(location)
	streetNames = re.findall(streetPattern, location)
	if len(streetNames) >= 2:
		return ' & '.join(sorted(streetNames[:2]))
	else:
		return location

addressCol = parkingData['Location'].apply(locationToAddress)

parkingData['address'] = addressCol

parkingData.to_csv('./parking2007_2008.csv')

amountsByLocation = parkingData[['address','Amount Due']]

statsByLocation = amountsByLocation.groupby('address').describe().unstack()

addressByTicketCounts = statsByLocation['Amount Due'].reset_index().sort('count', ascending=False)

addressByTicketCounts.to_csv('./address_by_ticket_counts_2007_2008.csv')

