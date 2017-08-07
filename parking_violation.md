
## This is a map of parking tickets issued in the city of Eugene in 2007-2008, based on data released by the city to the [2017 Hack For A Cause event]()
---
### What's the raw data like?
The original data was given to us as an Excel file made up of 3 separate sheets each containing data from different time periods. Putting them together, we get parking violation data from July of 2007 to June of 2008 in csv format: [csv data](https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/parking2007_2008.csv). Each record is stored in a row of this csv table. Let's write some code to load this csv file and look at the first few lines of this table:


```javascript/playable
// generate Markdown table using js
const originalParkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/parking2007_2008_raw.csv';
const myDiv = this.div;
let headerRow = '|';
let extraLine = '\n|';
let numRowsToShow = 10;

d3.csv(originalParkingCSV, function(data) {
  for (const key of d3.keys(data[0])) {
    headerRow += key+'|';
    extraLine += ':---|';
  }
  // console.log(headerRow, extraLine);

  const dataToShow = data.slice(1,numRowsToShow+1);

  let tableRows = dataToShow.map(function(row) {
    let oneRow = '\n|'
    for (const value of d3.values(row)) {
      oneRow += value+'|';
    }
    return oneRow;
  });

  let mdTable =
  `
  ${headerRow}${extraLine}${tableRows.join('')}
  `;
  // console.log(mdTbTemplate);
  let sdContent =
  `
  #### Raw data in csv format:
  ${mdTable}
  `;
  smartdown.setSmartdown(sdContent, myDiv);
  //smartdown.cellChanged('mdParkingDataTable', mdTbTemplate);
  //console.log(env.mdParkingDataTable);
});


```

To visualize this data, we will display on a map the **Location** of parking tickets, and ideally provide some statistics associated with the locations where parking tickets were most frequently issued.

---
### Data cleaning and getting locations geocoded (Python, pandas)
The main issue with the *Location* data is that it often consists of two or three street names. For example, 'KINCAID ST 11TH AVE 12TH'. This probably means the location of this parking violation is on Kincaid Street, between 11th and 12th Ave. While this format is human-readable and we could figure out what it means, it is not exact/accurate enough for the [Google geocoding API](https://developers.google.com/maps/documentation/geocoding/intro) to decipher.
Therefore I decided in this situation ('Location' madeup of more than 3 street names), I'll just take the first two street name and get the geolocation coordinates for where these two streets intercept from Google map.
Below is a Python script to transform the 'Location' column from our raw data into a more Google-readable 'address' column.

```python
#!usr/bin/python

import pandas as pd
import re

parkingData = pd.read_csv('./parking2007_2008_raw.csv')

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

parkingData.to_csv('./parking2007_2008_w_address.csv')

```
Now we can compare the 'Location' and the new 'address' column to get an idea of what we just did:

```javascript/playable
// compare the 'Location' column to the 'address' column of select rows
const originalParkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/parking2007_2008_w_address.csv';
const myDiv = this.div;
let headerRow = '|Location|Address';
let extraLine = '\n|:---|:---|';
let rowsToShow = [10,15];

d3.csv(originalParkingCSV, function(data) {
  const dataToShow = data.slice(rowsToShow[0], rowsToShow[1]);

  let tableRows = dataToShow.map(function(row) {
    let oneRow = '\n|'+row.Location+'|'+row.address+'|'
    return oneRow;
  });

  let mdTable =
  `
  ${headerRow}${extraLine}${tableRows.join('')}
  `;
  console.log(tableRows.join(''));
  let sdContent =
  `
  #### Compare the 'Location' in raw data to the transformed 'address' for geocoding:
  ${mdTable}
  `;
  smartdown.setSmartdown(sdContent, myDiv);
});

```
---

### Hit up Google geocoding API and get some coordinates (Python, geopy)

Because the Google geocoding API has a certain quota per request IP, I decided to find out which addresses were the most frequently ticketed locations and get the coordinates of those addresses.

```python
#!usr/bin/python

import pandas as pd
import re
from geopy.geocoders import GoogleV3
import pdb
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# -- Sort address by ticket count to find the most frequently ticketed locations -- #
amountsByLocation = parkingData[['address','Amount Due']]

statsByLocation = amountsByLocation.groupby('address').describe().unstack()

addressByTicketCounts = statsByLocation['Amount Due'].reset_index().sort('count', ascending=False)

addressByTicketCounts.to_csv('./address_by_ticket_counts_2007_2008.csv')

# -- Get the top N address geocoded -- #
addressByTicketCounts = pd.read_csv('./address_by_ticket_counts_2007_2008.csv')

geolocator = GoogleV3(api_key='AIzaSyDImvv3i9XUZLf8oDd6Of51_plddaJ9iC4', timeout=60)

# Get geolocation for the highest ranked 100 addresses by ticket number
numOfTopAddress = 100
topAddresses =  addressByTicketCounts.address[:numOfTopAddress]
topAddressCounts = addressByTicketCounts['count'][:numOfTopAddress]
topAddressMax = addressByTicketCounts['max'][:numOfTopAddress]

latitudeCol = np.empty(numOfTopAddress, dtype=float)
longitudeCol = np.empty(numOfTopAddress, dtype=float)

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

outputDf = pd.DataFrame({'address':topAddresses, 'count':topAddressCounts, 'max':topAddressMax, 'latitude':latitudeCol, 'longitude':longitudeCol})

outputDf.to_csv('./top_address_geocoded_2007_2008.csv')

```

---

### Let's make a map and put some markers on it (leaflet.js)
#### Here is a simple leaflet map centered on Eugene, OR.
```leaflet/playable
const mymap = L.map(this.div.id).setView([44.0489713,-123.0944854], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
}).addTo(mymap);

return mymap;
```
---

### What about adding some trend lines to show the number of tickets issued in each month?
#### Approach 1: Loading premade figures (Python matplotlib)
#### Approach 2: Dynamic loading of data and creating the figure when user clicks on icon (d3.js)
---

### The final map!
#### Click on an icon on the map to see ticket number over time:
```leaflet/playable/autoplay
const mymap = L.map(this.div.id).setView([44.0489713,-123.0944854], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
}).addTo(mymap);

// Preprocessing with Python to do geocoding, use the resulting latitude, longitude data for leaflet map.
// const parkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/parking_aggregate_2007_2008_geocoded.csv';

const parkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/top_addresses_parking_latlong_n_monthly_stats.csv';

mymap.on('popupopen', function (e) {
  console.log('popupopen');

  e.popup._source.showSVG();
});
mymap.on('popupclose',      function (e) { console.log('popupclose'); });

d3.csv(parkingCSV, function(d) {
  const countsByMonthColNames = d3.keys(d).filter(function(key) {
                        return ((key.indexOf("count") != -1) && (key.indexOf("count") != 0));
               });
  // console.log(countsByMonthColNames);
  const countsByMonth = countsByMonthColNames.map(function(name) {
      return +d[name];
    });

  return {
    address: d.address,
    latitude: +d.latitude,
    longitude: +d.longitude,
    totalCount: +d.count,
    maxTicket: +d.max,
    countsByMonth: countsByMonth
  };
}, function(data) {
   // console.log(data[0]);
   data.map(function(d,i) {
    // somehow d3.csv is treating missing cells as value 0?
    if (d.latitude != 0 && d.longitude != 0) {
      const marker = L.marker([d.latitude, d.longitude]).addTo(mymap);
      // const imgName = encodeURI(d.address);
      // const imgUrl = `https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/figures/${imgName}.png`;
      // console.log(imgUrl);
      marker.bindPopup(`<svg id="mysvg${i}"></svg><br><b>${d.address}</b><br>Number of tickets in 2007-2008: ${d.totalCount}.<br>Maximum fine: ${d.maxTicket}`);
      const dataToPlot = d.countsByMonth;
      // X scale will fit values within pixels 0-100
      const x = d3.scaleLinear().domain([1, dataToPlot.length]).range([40, 200]);
      // Y scale will fit values within pixels 0-100
      const y = d3.scaleLinear().domain(d3.extent(dataToPlot)).range([100, 10]);

      // create a line object that represents the SVN line we're creating
      const line = d3.line()
        .x(function(d,i) {
          return x(i);
          })
        .y(function(d) {
          return y(d);
          })

      marker.showSVG = function() {
        const margin = {top: 20, right: 40, bottom: 10, left: 40};
    	const width = 300 - margin.left - margin.right;
    	const height = 150 - margin.top - margin.bottom;
        const svg = d3.select(`#mysvg${i}`)
                  .attr("width", width + margin.left + margin.right)
                  .attr("height", height + margin.top + margin.bottom);
        console.log(dataToPlot);
        svg.append("path")
          .attr("class", "line")
          .attr("d", line(dataToPlot))
	  .attr("stroke-width", "2")
	  .attr("stroke", "black")
	  .attr("fill", "none");

	svg.selectAll("dot")
	      .data(dataToPlot)
      	   .enter().append("circle")
              .attr("r", 3.5)
              .attr("cx", function(d,i) { return x(i); })
              .attr("cy", function(d) { return y(d); });
      };

    }
  });
});

return mymap;

```


