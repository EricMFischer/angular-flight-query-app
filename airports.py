from collections import Counter
import csv

flight_counts = Counter()
with open('flights.csv', 'rU') as infile:
    csvreader = csv.reader(infile)
    csvreader.next()
    for row in csvreader:
        orig_dest = (row[0], row[1])
        flight_counts.update(orig_dest)

with open('flight_counts.csv', 'w') as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerow(["code", "count"])
    for code, count in flight_counts.items():
        csvwriter.writerow([code, count])


<script>
  var width = 960,
      height = 600;

  var path = d3.geo.path()
      .projection(null);

  var svg = d3.select("body").append("svg")
      .attr("width", width)
      .attr("height", height);

  d3.json("us.json", function(error, us) {
    if (error) return console.error(error);
    
    // code for base map
    svg.append("path")
      .datum(topojson.feature(us, us.objects.nation))
      .attr("class", "land")
      .attr("d", path);

    // code for base map
    svg.append("path")
      .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
      .attr("class", "border border--state")
      .attr("d", path);

    // place bubbles at each county centroid
    svg.append("g")
      .attr("class", "bubble")
      .selectAll("circle")
      .data(topojson.feature(us, us.objects.counties).features)
      .enter().append("circle")
      .attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
      .attr("r", 1.5);

    // so that circles' areas are proportional to size of the population
    var radius = d3.scale.sqrt()
      .domain([0, 1e6])
      .range([0, 13]);

    // reduces occlusion by sorting bubbles by descending size
    // smaller bubbles are drawn on top of larger bubbles
    svg.append("g")
      .attr("class", "bubble")
      .selectAll("circle")
      .data(topojson.feature(us, us.objects.counties).features
      .sort(function(a, b) { return b.properties.population - a.properties.population; }))
      .enter().append("circle")
      .attr("transform", function(d) { return "translate(" + path.centroid(d) + ")"; })
      .attr("r", function(d) { return radius(d.properties.population); });

    // legend displays 3 circles and their associated population sizes
    var legend = svg.append("g")
      .attr("class", "legend")
      .attr("transform", "translate(" + (width - 50) + "," + (height - 20) + ")")
      .selectAll("g")
      .data([1e6, 3e6, 6e6])
      .enter().append("g");

    legend.append("circle")
      .attr("cy", function(d) { return -radius(d); })
      .attr("r", radius);

    legend.append("text")
      .attr("y", function(d) { return -2 * radius(d); })
      .attr("dy", "1.3em")
      .text(d3.format(".1s"));
  });
</script>