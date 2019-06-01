/*****************************

Pulls the metadata and displays it on the index page

*****************************/
function buildMetadata(sample) {
  // Use `d3.json` to fetch the metadata for a sample
  var metadata = d3.select("#sample-metadata");
  var url = "/metadata/" + sample;
  console.log(url)
  // document.getElementById("#sample-metadata").innerHTML = "";
  d3.json(url).then(function(response) {
    console.log(response);
    $("#sample-metadata").empty();
    Object.entries(response).forEach(([key, value]) => metadata.append("p").text(`${key}: ${value}`));
  });
}


/*****************************

Builds the pie Charts

******************************/

function buildCharts(sample) {
  
  var url = "/samples/" + sample;

  d3.json(url).then(function(response) {
    console.log(response);

    d3.select("#pie > *").remove();
    
    yellow = response.yellow_cards; 
    direct_red = response.direct_red_cards;
    indirect_red = response.indirect_red_cards; 
    not_disciplined = response.no_action;
    suffered = response.suffered_f;


    var yellow_percent = Number; 
    var direct_red_percent = Number;
    var no_action_percent = Number;
    var indirect_red_percent = Number;


    yellow_percent = Math.round((yellow / response.comitted_f) * 100);
    direct_red_percent = Math.round((direct_red / response.comitted_f) * 100);
    no_action_percent = Math.round((not_disciplined / response.comitted_f) * 100);
    indirect_red_percent = Math.round((indirect_red / response.comitted_f) * 100);


    var data2 = [
      {card_type: "Yellow", count: yellow, percentage: yellow_percent, color: '#8ABD4A'}, 
      {card_type: "Red", count: direct_red, percentage: direct_red_percent, color: '#f8b70a'},
      {card_type: "Indirect Red", count: indirect_red, percentage: indirect_red_percent, color: '#9f8170'}, 
      {card_type: "N.D.", count: not_disciplined, percentage: no_action_percent, color: '#6149c6'},
    ];

   
    var width = 450
    height = 450
    margin = 50;

    // The radius of the pieplot is half the width or half the height (smallest one). I substract a bit of margin.
    var radius = Math.min(width, height) / 2 - margin

    var arc = d3.arc()
    	.outerRadius(radius - 10)
    	.innerRadius(0);

		var pie = d3.pie()
	    .sort(null)
	    .value(function(d) {
	        return d.count;
	    });

		var svg = d3.select('#pie').append("svg")
	    .attr("width", width)
	    .attr("height", height)
	    .append("g")
	    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var g = svg.selectAll(".arc")
      .data(pie(data2))
      .enter().append("g");    

   	g.append("path")
    	.attr("d", arc)
      .style("fill", function(d,i) {
      	return d.data.color;
      });

    g.append("text")
    	.attr("transform", function(d) {
        var _d = arc.centroid(d);
        _d[0] *= 2.2;	//multiply by a constant factor
        _d[1] *= 2.2;	//multiply by a constant factor
        return "translate(" + _d + ")";
      })
      .attr("dy", ".50em")
      .style("text-anchor", "middle")
      .text(function(d) {
        if(d.data.percentage < 3) {
          return '';
        }
        return d.data.card_type + "\n" + d.data.percentage + '%';
      });
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildMetadata(newSample);
  buildCharts(newSample);
};

// Initialize the dashboard
init();
