#!usr/bin/python

import pandas as pd
import re
import pdb
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

addressByTicketCounts = pd.read_csv('./address_by_ticket_counts_2007_2008.csv')
parkingData = pd.read_csv('./parking2007_2008.csv')

# Get geolocation for the highest ranked 100 addresses by ticket number
numOfTopAddress = 100
topAddresses =  addressByTicketCounts.address[:numOfTopAddress]
topCounts = addressByTicketCounts['count'][:numOfTopAddress]
topAddressMax = addressByTicketCounts['max'][:numOfTopAddress]


for ind,address in topAddresses.iteritems():
    datesThisAddress = parkingData.loc[parkingData.address==address][['Date','Amount Due']]
    datesThisAddress['Date'] = pd.to_datetime(datesThisAddress['Date'])
    datesThisAddress.set_index('Date', inplace=True)
    amountDueEachMonth = datesThisAddress.groupby(pd.TimeGrouper(freq='M')).agg(['sum','count']) #group by month and aggregate on sum of ticket amount due and number of tickets
    #pdb.set_trace()
    # Convert each address's stats into columns
    statsThisAddress = amountDueEachMonth.T.unstack(level=-1).rename(index={'Amount Due': address}) #The resulting dataframe has this address as index and multi-level column first level being date (by month), second level being 'sum' and 'count'
    if ind == 0:
        outputDf = statsThisAddress
    else:
        outputDf = pd.concat([outputDf, statsThisAddress])
    #pdb.set_trace()
    #countByDate = datesThisAddress.value_counts().sort_index(ascending=True)
    #datesToPlot = countByDate.index
    #countsToPlot = countByDate.values
    #datesToPlot = matplotlib.dates.date2num(datetimes)
    #plt.clf()
    #print 'plotting figure for {}'.format(address)
    #trendLinePlot = plt.plot(datesToPlot, countsToPlot, 'k.-')
    #plt.ylabel('Tickets per day')
    #plt.savefig('./figures/{}.png'.format(address))

outputDf.to_csv('./ticket_counts_n_total_fine_by_month_2007_2008.csv')


'''
batchSize = 200
numBatch = int(np.ceil(len(ticketAmountByLocation)/float(batchSize)))
outFile = './parking_aggregate_2007_2008_geocoded.csv'

for batch in range(numBatch):
	thisBatch = ticketAmountByLocation[batch*batchSize: (batch+1)*batchSize]
	addressCol = pd.Series(index=thisBatch.index, dtype=object)
	latitudeCol = pd.Series(index=thisBatch.index, dtype=float)
	longitudeCol = pd.Series(index=thisBatch.index, dtype=float)
	print 'processing batch {}'.format(batch)

	for ind, location in thisBatch.Location.iteritems():
		streetPattern = re.compile('[A-Z0-9]+(?=\sAVE|\sST)')
		streetNames = re.findall(streetPattern, location)
		if len(streetNames) >= 2:
			address = ' & '.join(sorted(streetNames[:2]))
		else:
			address = location

		addressCol[ind] = address
		fullAddress = address + ', Eugene, OR'
		print 'Geocoding {}'.format(fullAddress)
		results = geolocator.geocode(fullAddress, exactly_one=True)
		if (results != None):
			address, (latitude, longitude) = results
			latitudeCol[ind] = latitude
			longitudeCol[ind] = longitude
		else:
			latitudeCol[ind] = np.NaN
			longitudeCol[ind] = np.NaN
		#pdb.set_trace()

	thisBatch['address'] = addressCol.values
	thisBatch['latitude'] = latitudeCol.values
	thisBatch['longitude'] = longitudeCol.values

	if batch == 0:
		with open(outFile,'w') as f:
			thisBatch.to_csv(f)
	else:
		with open(outFile,'a') as f:
			thisBatch.to_csv(f, header=False)

	time.sleep(60)

'''
