
## This is a map of parking tickets issued in the city of Eugene in 2007-2008, based on data released by the city to the [2017 Hack For A Cause event]()
---
### What's the raw data like?

### Data cleaning and getting locations geocoded 

### Let's make a map

### The finished prodcut!
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


