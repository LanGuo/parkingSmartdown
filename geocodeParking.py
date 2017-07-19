#!usr/bin/python

import pandas as pd
import re
from geopy.geocoders import GoogleV3
import pdb
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

addressByTicketCounts = pd.read_csv('./address_by_ticket_counts_2007_2008.csv')
parkingData = pd.read_csv('./parking2007_2008.csv')

geolocator = GoogleV3(api_key='AIzaSyDImvv3i9XUZLf8oDd6Of51_plddaJ9iC4', timeout=60)

# Get geolocation for the highest ranked 100 addresses by ticket number
top100Addresses =  addressByTicketCounts.address[:100]
top100Counts = addressByTicketCounts['count'][:100]
top100Max = addressByTicketCounts['max'][:100]
latitudeCol = np.empty(100, dtype=float)
longitudeCol = np.empty(100, dtype=float)

for ind,address in top100Addresses.iteritems():
    fullAddress = address + ', Eugene, OR'
    print 'Geocoding {}'.format(fullAddress)
    results = geolocator.geocode(fullAddress, exactly_one=True)
    if (results != None):
        fullAddress, (latitude, longitude) = results
        latitudeCol[ind] = latitude
        longitudeCol[ind] = longitude
    else:
        latitudeCol[ind] = np.NaN
        longitudeCol[ind] = np.NaN
    
    datesThisAddress = parkingData.loc[parkingData.address==address]['Date']
    datesThisAddress = datesThisAddress.apply(lambda x: datetime.strptime(x.split(' ')[0], '%m/%d/%y')) #convert date strings to datetime objects
    countByDate = datesThisAddress.value_counts().sort_index(ascending=True)
    datesToPlot = countByDate.index
    countsToPlot = countByDate.values
    #datesToPlot = matplotlib.dates.date2num(datetimes)
    plt.clf()
    print 'plotting figure for {}'.format(address)
    trendLinePlot = plt.plot(datesToPlot, countsToPlot, 'k.-')
    plt.ylabel('Tickets per day')
    plt.savefig('./figures/{}.png'.format(address))

outputDf = pd.DataFrame({'address':top100Addresses, 'count':top100Counts, 'max':top100Max, 'latitude':latitudeCol, 'longitude':longitudeCol})

outputDf.to_csv('./top_100_address_geocoded_2007_2008.csv')


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
