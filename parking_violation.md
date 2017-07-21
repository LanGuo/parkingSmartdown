
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

const parkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/top_100_address_geocoded_2007_2008.csv';
const statsByMonthCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/ticket_counts_n_total_fine_by_month_2007_2008.csv';

d3.csv(parkingCSV, function(d) {
  return {
    address: d.address,
    latitude: +d.latitude,
    longitude: +d.longitude,
    count: +d.count,
    max_ticket: +d.max
  };
}, function(data) {
  console.log(data[0]);
  data.map(function(d,i) {
    // somehow d3.csv is treating missing cells as value 0?
    if (d.latitude != 0 && d.longitude != 0) {
      const marker = L.marker([d.latitude, d.longitude]).addTo(mymap);
      // const imgName = encodeURI(d.address);
      // const imgUrl = `https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/figures/${imgName}.png`;
      // console.log(imgUrl);
      // marker.bindPopup(`<img src=${imgUrl}></img><b>${d.address}</b><br>Number of tickets in 2007-2008: ${d.count}.<br>Maximum fine: ${d.max_ticket}`);
      marker.bindPopup(`<b>${d.address}</b><br>Number of tickets in 2007-2008: ${d.count}.<br>Maximum fine: ${d.max_ticket}`);
    }
  })
});

d3.csv(statsByMonthCSV, 
  function(d) {
    const countsColNames = d3.keys(d).filter(function(key) { 
  		     	     return key.indexOf("count") != -1; 
			   });
    console.log(countsColNames);
    const counts = countsColNames.map(function(name) { 
      return +d[name]
    });
    console.log(counts); 
    // console.log(d.address);
    return {
      d.address = d.address;
      d.counts = counts
    }; 
  },
  function(data) {
    console.log(data[0]);
  }
);
 
return mymap;

```


