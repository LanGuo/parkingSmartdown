### Plotly bar graph of total ticket numbers from the top 100 ticketed locations, displayed by month from the period July 2007 to June 2008
```plotly/playable/autoplay
const parkingCSV = 'https://raw.githubusercontent.com/LanGuo/parkingSmartdown/master/top_addresses_parking_latlong_n_monthly_stats.csv';

const myDiv = this.div;
// console.log(myDiv);
 
d3.csv(parkingCSV, function(d) {
  const countsByMonthColNames = d3.keys(d).filter(function(key) {
                        return ((key.indexOf("count") != -1) && (key.indexOf("count") != 0));
               });
  // console.log(countsByMonthColNames);
  let newRow = {};
  countsByMonthColNames.forEach(function(name) {
    const month = name.split('_')[0];
    newRow[month] = +d[name];
    });
  // console.log(newRow);    
  return newRow;
}, function(data) {
   // console.log(data[0]);
   const x = []; 
   const y = [];
   for (let key of d3.keys(data[0])) {
     x.push(key);
     y.push(d3.sum(data, function(d) { return d[key]; }));
   }  

   const dataToPlot = [
     {
       x: x,
       y: y,
       type: 'bar'
     }
   ];

  Plotly.newPlot(myDiv, dataToPlot);
});

```
