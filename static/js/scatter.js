// var graphData = {{ data.chart_data | safe }}

d3.csv('db/data.csv', function(data){

    var width = parseInt(d3.select("#pie").style("width"));


    // Designate the height of the graph
    var height = width - width / 3.0;

    // Margin spacing for graph
    var margin = 20;

    // space for placing words
    var labelArea = 110;

    // padding for the text at the bottom and left axes
    var tPadBot = 40;
    var tPadLeft = 40;

    var svg = d3
    .select("#pie")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "chart");

    var circRadius;
    function crGet() {
    if (width <= 530) {
        circRadius = 10;
    }
    else {
        circRadius = 15;
    }
    }
    crGet();

    svg.append("g").attr("class", "xText");
    var xText = d3.select(".xText");

    function xTextRefresh() {
    xText.attr(
        "transform",
        "translate(" +
        ((width - labelArea) / 2 + labelArea) +
        ", " +
        (height - margin - tPadBot) +
        ")"
    );
    }
    xTextRefresh();

    xText
    .append("text")
    .attr("y", -26)
    .attr("data-name", "played")
    .attr("data-axis", "x")
    .attr("class", "aText active x")
    .text("Matches Played");

    var leftTextX = margin + tPadLeft;
    var leftTextY = (height + labelArea) / 2 - labelArea;

    svg.append("g").attr("class", "yText");

    var yText = d3.select(".yText");

    function yTextRefresh() {
    yText.attr(
        "transform",
        "translate(" + leftTextX + ", " + leftTextY + ")rotate(-90)"
    );
    }
    yTextRefresh();

    yText
    .append("text")
    .attr("y", -26)
    .attr("data-name", "comitted_f")
    .attr("data-axis", "y")
    .attr("class", "aText active y")
    .text("Fouls Commited");

    yText
    .append("text")
    .attr("x", 0)
    .attr("data-name", "suffered_f")
    .attr("data-axis", "y")
    .attr("class", "aText inactive y")
    .text("Fouls Suffered");


    function visualize(theData) {
    var curX = "played";
    var curY = "comitted_f";
    var xMin;
    var xMax;
    var yMin;
    var yMax;

    var toolTip = d3
        .tip()
        .attr("class", "d3-tip")
        .offset([40, -60])
        .html(function(d) {
        var theX;
        var theState = "<div>" + d.country + "</div>";
        var theY = "<div>" + curY + ": " + d[curY] + "</div>";
        if (curX === "played") {
            // Grab the x key and a version of the value formatted to show percentage
            theX = "<div>" + curX + ": " + d[curX] + "</div>";
        }
        else {
            // Otherwise
            // Grab the x key and a version of the value formatted to include commas after every third digit.
            theX = "<div>" +
            curX +
            ": " +
            parseFloat(d[curX]).toLocaleString("en") +
            "</div>";
    }
    return theState + theX + theY;
    });

svg.call(toolTip);

function xMinMax() {
    // min will grab the smallest datum from the selected column.
    xMin = d3.min(theData, function(d) {
    return parseFloat(d[curX]) * 0.90;
    });

    // .max will grab the largest datum from the selected column.
    xMax = d3.max(theData, function(d) {
    return parseFloat(d[curX]) * 1.10;
    });
}

function yMinMax() {
    // min will grab the smallest datum from the selected column.
    yMin = d3.min(theData, function(d) {
    return parseFloat(d[curY]) * 0.90;
    });

    // .max will grab the largest datum from the selected column.
    yMax = d3.max(theData, function(d) {
    return parseFloat(d[curY]) * 1.10;
    });
}

function labelChange(axis, clickedText) {
    // Switch the currently active to inactive.
    d3
    .selectAll(".aText")
    .filter("." + axis)
    .filter(".active")
    .classed("active", false)
    .classed("inactive", true);

    // Switch the text just clicked to active.
    clickedText.classed("inactive", false).classed("active", true);
}

xMinMax();
yMinMax();

var xScale = d3
    .scaleLinear()
    .domain([xMin, xMax])
    .range([margin + labelArea, width - margin]);
var yScale = d3
    .scaleLinear()
    .domain([yMin, yMax])
    // Height is inverses due to how d3 calc's y-axis placement
    .range([height - margin - labelArea, margin]);

var xAxis = d3.axisBottom(xScale);
var yAxis = d3.axisLeft(yScale);

function tickCount() {
    if (width <= 500) {
    xAxis.ticks(5);
    yAxis.ticks(5);
    }
    else {
    xAxis.ticks(10);
    yAxis.ticks(10);
    }
}
tickCount();

svg
    .append("g")
    .call(xAxis)
    .attr("class", "xAxis")
    .attr("transform", "translate(0," + (height - margin - labelArea) + ")");
svg
    .append("g")
    .call(yAxis)
    .attr("class", "yAxis")
    .attr("transform", "translate(" + (margin + labelArea) + ", 0)");

var theCircles = svg.selectAll("g theCircles").data(theData).enter();

theCircles
    .append("circle")
    // These attr's specify location, size and class.
    .attr("cx", function(d) {
    return xScale(d[curX]);
    })
    .attr("cy", function(d) {
    return yScale(d[curY]);
    })
    .attr("r", circRadius)
    .attr("class", function(d) {
    return "stateCircle " + d.id;
    })
    // Hover rules
    .on("mouseover", function(d) {
    // Show the tooltip
    toolTip.show(d, this);

    // Highlight the state circle's border
    d3.select(this).style("stroke", "#323232");
    })
    .on("mouseout", function(d) {
    // Remove the tooltip
    toolTip.hide(d);
    // Remove highlight
    d3.select(this).style("stroke", "#e3e3e3");
    });

theCircles
    .append("text")
    // We return the abbreviation to .text, which makes the text the abbreviation.
    .text(function(d) {
    return d.country;
    })
    // Now place the text using our scale.
    .attr("dx", function(d) {
    return xScale(d[curX]);
    })
    .attr("dy", function(d) {
    // When the size of the text is the radius,
    // adding a third of the radius to the height
    // pushes it into the middle of the circle.
    return yScale(d[curY]) + circRadius / 2.5;
    })
    .attr("font-size", circRadius)
    .attr("class", "stateText")
    // Hover Rules
    .on("mouseover", function(d) {
    // Show the tooltip
    toolTip.show(d);
    // Highlight the state circle's border
    d3.select("." + d.country).style("stroke", "#323232");
    })
    .on("mouseout", function(d) {
    // Remove tooltip
    toolTip.hide(d);
    // Remove highlight
    d3.select("." + d.country).style("stroke", "#e3e3e3");
    });


d3.selectAll(".aText").on("click", function(){
    var self = d3.select(this);

    if (self.classed("inactive")) {
    // Grab the name and axis saved in label.
    var axis = self.attr("data-axis");
    var name = self.attr("data-name");

    // When x is the saved axis, execute this:
    if (axis === "x") {
        // Make curX the same as the data name.
        curX = name;

        // Change the min and max of the x-axis
        xMinMax();

        // Update the domain of x.
        xScale.domain([xMin, xMax]);

        // Now use a transition when we update the xAxis.
        svg.select(".xAxis").transition().duration(300).call(xAxis);

        // With the axis changed, let's update the location of the state circles.
        d3.selectAll("circle").each(function() {
        // Each state circle gets a transition for it's new attribute.
        // This will lend the circle a motion tween
        // from it's original spot to the new location.
        d3
            .select(this)
            .transition()
            .attr("cx", function(d) {
            return xScale(d[curX]);
            })
            .duration(300);
        });

        // We need change the location of the state texts, too.
        d3.selectAll(".stateText").each(function() {
        // We give each state text the same motion tween as the matching circle.
        d3
            .select(this)
            .transition()
            .attr("dx", function(d) {
            return xScale(d[curX]);
            })
            .duration(300);
        });

        // Finally, change the classes of the last active label and the clicked label.
        labelChange(axis, self);
    }
    else {
        // When y is the saved axis, execute this:
        // Make curY the same as the data name.
        curY = name;

        // Change the min and max of the y-axis.
        yMinMax();

        // Update the domain of y.
        yScale.domain([yMin, yMax]);

        // Update Y Axis
        svg.select(".yAxis").transition().duration(300).call(yAxis);

        // With the axis changed, let's update the location of the state circles.
        d3.selectAll("circle").each(function() {
        // Each state circle gets a transition for it's new attribute.
        // This will lend the circle a motion tween
        // from it's original spot to the new location.
        d3
            .select(this)
            .transition()
            .attr("cy", function(d) {
            return yScale(d[curY]);
            })
            .duration(300);
        });

        // We need change the location of the state texts, too.
        d3.selectAll(".stateText").each(function() {
        // We give each state text the same motion tween as the matching circle.
        d3
            .select(this)
            .transition()
            .attr("dy", function(d) {
            return yScale(d[curY]) + circRadius / 3;
            })
            .duration(300);
        });

        // Finally, change the classes of the last active label and the clicked label.
        labelChange(axis, self);
    }
    }
});



}

visualize(graphData);

}); 

