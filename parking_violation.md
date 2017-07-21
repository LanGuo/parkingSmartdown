
# This is a map of parking tickets issued in the city of Eugene in 2007-2008, based on data released by the city to the [2017 Hack For A Cause event]()
---

## Click on an icon on the map to see ticket number over time:
```leaflet/playable/autoplay

const mymap = L.map(this.div.id).setView([44.0489713,-123.0944854], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
}).addTo(mymap);

// Preprocessing with Python to do geocoding, use the resulting latitude, longitude data for leaflet map.
// const parkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/parking_aggregate_2007_2008_geocoded.csv';

const parkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/top_addresses_parking_latlong_n_monthly_stats.csv';

d3.csv(parkingCSV, function(d) {
  const countsByMonthColNames = d3.keys(d).filter(function(key) { 
  		     	     return (key.indexOf("count") != -1) && (key.indexOf("count") != 0); 
			   });
  console.log(countsColNames);
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
  console.log(data[0]);
});


 
return mymap;

```


/*
  data.map(function(d,i) {
    // somehow d3.csv is treating missing cells as value 0?
    if (d.latitude != 0 && d.longitude != 0) {
      const marker = L.marker([d.latitude, d.longitude]).addTo(mymap);
      // const imgName = encodeURI(d.address);
      // const imgUrl = `https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/figures/${imgName}.png`;
      // console.log(imgUrl);
      marker.bindPopup(`<div id="graph"></div><b>${d.address}</b><br>Number of tickets in 2007-2008: ${d.totalCount}.<br>Maximum fine: ${d.maxTicket}`);
      const graph = d3.select("#graph").append("svg:svg").attr("width", "100%").attr("height", "100%");

      // create a simple data array that we'll plot with a line (this array represents only the Y values, X will just be the index location)
      const data = d.countsByMonth;

      // X scale will fit values from 0-10 within pixels 0-100
      const x = d3.scale.linear().domain([0, 10]).range([0, 50]);
      // Y scale will fit values from 0-10 within pixels 0-100
      const y = d3.scale.linear().domain([0, 10]).range([0, 30]);

      // create a line object that represents the SVN line we're creating
      const line = d3.svg.line()
 	 // assign the X function to plot our line as we wish
		.x(function(d,i) { 
	 // verbose logging to show what's actually being done
	          console.log('Plotting X value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
	 // return the X coordinate where we want to plot this datapoint
	          return x(i); 
		  })
		.y(function(d) { 
	 // verbose logging to show what's actually being done
		  console.log('Plotting Y value for data point: ' + d + ' to be at: ' + y(d) + " using our yScale.");
	 // return the Y coordinate where we want to plot this datapoint
		  return y(d); 
		  })
	
	 // display the line by appending an svg:path element with the data line we created above
	 graph.append("svg:path").attr("d", line(data));
    }
  })
*/