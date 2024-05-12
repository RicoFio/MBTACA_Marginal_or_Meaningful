<script>
    import * as d3 from "d3";
    import {onMount} from "svelte";

    let margin;
    let width;
    let height;
    let svg;
    let donutData;
    let colorScale;

    onMount(() => {
        margin = {left: 20, top: 20, right: 20, bottom: 20};
        width = 500 - margin.left - margin.right;
        height = 500 - margin.top - margin.bottom;

        svg = d3.select("#chart").append("svg")
            .attr("width", (width + margin.left + margin.right))
            .attr("height", (height + margin.top + margin.bottom))
            .append("g").attr("class", "wrapper")
            .attr("transform", "translate(" + (width / 2 + margin.left) + "," + (height / 2 + margin.top) + ")");

        //Some random data
        donutData = [
            {name: "Antelope", value: 15},
            {name: "Bear", value: 9},
            {name: "Cheetah", value: 19},
            {name: "Dolphin", value: 12},
            {name: "Elephant", value: 14},
            {name: "Flamingo", value: 21},
            {name: "Giraffe", value: 18},
            {name: "Other", value: 8}
        ];

        //Create a color scale
        colorScale = d3.scaleLinear()
            .domain([1, 3.5, 6])
            .range(["#2c7bb6", "#ffffbf", "#d7191c"])
            .interpolate(d3.interpolateHcl);

        //Turn the pie chart 90 degrees counter clockwise, so it starts at the left
        let pie1 = d3.pie()
            .startAngle(-90 * Math.PI / 180)
            .endAngle(-90 * Math.PI / 180 + 2 * Math.PI)
            .value(function (d) {
                return d.value;
            })
            .padAngle(.01)
            .sort(null);

        let pie2 = d3.pie()
            .startAngle(-90 * Math.PI / 180)
            .endAngle(-90 * Math.PI / 180 + 2 * Math.PI)
            .value(function (d) {
                return d.value;
            })
            .padAngle(.01)
            .sort(null);

        //////////////////////////////////////////////////////////////
        //////////////////// Create Donut Chart //////////////////////
        //////////////////////////////////////////////////////////////

        //Create the donut slices and also the invisible arcs for the text
        createDonutSlices(pie1, 150, 200);
        appendLables(pie1, 150, 200);

        createDonutSlices(pie2, 50, 120);
        appendLables(pie2, 50, 120);
    })

    function arc (innerRadius, outerRadius) {
        return d3
            .arc()
            .innerRadius(innerRadius) // This is the size of the donut hole
            .outerRadius(outerRadius);
    }

    function createDonutSlices(pie, innerRadius, outerRadius) {
        svg.selectAll(".donutArcs")
            .data(pie(donutData))
            .enter().append("path")
            .attr("class", "donutArcs")
            .attr("d", arc(innerRadius, outerRadius))
            .style("fill", function (d, i) {
                if (i === 7) return "#CCCCCC"; //Other
                else return colorScale(i);
            })
            .each(function (d, i) {
                //Search pattern for everything between the start and the first capital L
                var firstArcSection = /(^.+?)L/;

                //Grab everything up to the first Line statement
                var newArc = firstArcSection.exec(d3.select(this).attr("d"))[1];
                //Replace all the comma's so that IE can handle it
                newArc = newArc.replace(/,/g, " ");

                //If the end angle lies beyond a quarter of a circle (90 degrees or pi/2)
                //flip the end and start position
                if (d.endAngle > 90 * Math.PI / 180) {
                    var startLoc = /M(.*?)A/,		//Everything between the first capital M and first capital A
                        middleLoc = /A(.*?)0 0 1/,	//Everything between the first capital A and 0 0 1
                        endLoc = /0 0 1 (.*?)$/;	//Everything between the first 0 0 1 and the end of the string (denoted by $)
                    //Flip the direction of the arc by switching the start en end point (and sweep flag)
                    //of those elements that are below the horizontal line
                    var newStart = endLoc.exec(newArc)[1];
                    var newEnd = startLoc.exec(newArc)[1];
                    var middleSec = middleLoc.exec(newArc)[1];

                    //Build up the new arc notation, set the sweep-flag to 0
                    newArc = "M" + newStart + "A" + middleSec + "0 0 0 " + newEnd;
                }//if

                //Create a new invisible arc that the text can flow along
                svg.append("path")
                    .attr("class", "hiddenDonutArcs")
                    .attr("id", "donutArc" + i)
                    .attr("d", newArc)
                    .style("fill", "none");
            });
    }

    function appendLables(pie) {
        //Append the label names on the outside
        svg.selectAll(".donutText")
            .data(pie(donutData))
            .enter().append("text")
            .attr("class", "donutText")
            //Move the labels below the arcs for those slices with an end angle greater than 90 degrees
            .attr("dy", function (d, i) {
                return (d.endAngle > 90 * Math.PI / 180 ? 18 : -11);
            })
            .append("textPath")
            .attr("startOffset", "50%")
            .style("text-anchor", "middle")
            .attr("xlink:href", function (d, i) {
                return "#donutArc" + i;
            })
            .text(function (d) {
                return d.data.name;
            });
    }
</script>

<div id="chart"></div>

<style>
    #chart {
        z-index: 1000;
        fill: #ffffff;
        font-size: 16px;
        color: #f0f0f0;
        text-align: center;
    }

    .donutText {
        z-index: 1000;
        color: #ffffff;
    }
</style>
