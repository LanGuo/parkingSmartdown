#!usr/bin/python

import pandas as pd
import re
from geopy.geocoders import GoogleV3
import pdb
import numpy as np
import time

ticketAmountByLocation = pd.read_csv('./parking_aggregate_2007_2008.csv')
geolocator = GoogleV3(api_key='AIzaSyDImvv3i9XUZLf8oDd6Of51_plddaJ9iC4', timeout=60)
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
			address = ' & '.join(streetNames)
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

	thisBatch.address = addressCol
	thisBatch.latitude = latitudeCol
	thisBatch.longitude = longitudeCol

	if batch == 0:
		with open(outFile,'w') as f:
			thisBatch.to_csv(f)
	else:
		with open(outFile,'a') as f:
			thisBatch.to_csv(f, header=False)

	time.sleep(60)
