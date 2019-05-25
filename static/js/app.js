// Pulls the metadata and displays it on the index page
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

// Builds the current pie graphs 
function buildCharts(sample) {
  
  var url = "/samples/" + sample;

  d3.json(url).then(function(response) {
    console.log(response);

    var yellow_cards = Number;
    var direct_red_cards = Number;
    var indirect_red_cards = Number;
    var no_action = Number;
    var suffered_f = Number;

    yellow = response.yellow_cards; 
    direct_red = response.direct_red_cards;
    indirect_red = response.indirect_red_cards; 
    not_disciplined = response.no_action;
    suffered = response.suffered_f;

    var data1 = [yellow, direct_red, indirect_red, not_disciplined];
    
    console.log(data1);

    var data = [{
      values: data1, 
      labels: ['Yellow Cards', 'Direct Red Cards', 'Indirect Red Cards', 'No Cards Given'],
      type: 'pie'
    }];

    var layout = {
      height: 400,
      width: 500
    };

    Plotly.newPlot('bubble', data, layout);
  
  });
}

// Builds the scatter plot
function buildscatter(){
  var url = "/scatter";

  d3.json(url).then(function(response) {
    console.log(response);
  
    var trace2 = [{
      x: response.played,
      y: response.comitted_f,
      text: response.country,
      mode: 'markers+text', 
      textposition: 'top center', 
      type: "scatter",
      marker: {size:12}
    }]

    var layout2 = {
      title: 'Bubble chart for each sample',
      showlegend: false,
      height: 600,
      width: 1400
    };

    console.log(trace2);
    Plotly.newPlot('pie', trace2, layout2);

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
    console.log(firstSample)
    
    buildCharts(firstSample);
    buildMetadata(firstSample);

    buildscatter();
    
    
    // Hopefully this creates the D3 Graph
    // d3ScatterPlot();
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildMetadata(newSample);
  
  buildCharts(newSample);
}

// Initialize the dashboard
init();
