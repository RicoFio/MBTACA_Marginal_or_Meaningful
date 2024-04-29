<!-- TreemapUsage.svelte -->

<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
  
    export let data = [];
    let svgId = 'treemap-usage-svg'; // Unique ID for the SVG
  
    onMount(() => {
        drawTreemap();
    });
  function drawTreemap() {
          const width = 400;
          const height = 250;
  
          const svg = d3
              .select(`#${svgId}`) // Use the unique ID for selection
              .attr("width", width)
              .attr("height", height);
  
  
          // Transform data into hierarchy
          const root = d3.hierarchy({ children: data }).sum((d) => d.value);
  
        //   console.log("U: Data being passed to TreeMap component:", data); // Add console log here
  
          // Create treemap layout
          const treemap = d3.treemap().size([width, height]).padding(1);
  
          // Compute treemap layout
          treemap(root);
  
          // Create cells for each data point
          const cell = svg
              .selectAll("g")
              .data(root.leaves())
              .enter()
              .append("g")
              .attr("transform", (d) => `translate(${d.x0},${d.y0})`);
  
          // Append rectangle for each cell
          cell.append("rect")
              .attr("width", (d) => d.x1 - d.x0)
              .attr("height", (d) => d.y1 - d.y0)
              .attr("fill", (d) => getColorByCategory(d.data))
              .on("mouseover", handleMouseOver)
              .on("mouseout", handleMouseOut);
  
          // Append text for each cell
          cell.append("text")
              .attr("x", 5)
              .attr("y", 15)
              .text((d) => d.data.name)
              .attr("fill", "white");
  
          cell.append("text")
              .attr("x", 5)
              .attr("y", 40)
              .text((d) => `${((d.value / root.value) * 100).toFixed(1)}%`)
              .attr("fill", "white");
  
          function handleMouseOver() {
              d3.select(this).attr("fill", "orange");
          }
  
          function handleMouseOut() {
              d3.select(this).attr("fill", (d) => getColorByCategory(d.data));
          }
      }
  
      function getColorByCategory(d) {
          switch (d.category1) {
              case "pctUsedAsSF":
                  return "#05515e";
              case "pctUsedAsComm":
                  return "#629681";
              case "pctUsedAsMulti":
                  return "#a9987a";
              case "pctUsedAsDuplex":
                  return "#9f9090";
              case "pctUsedAsTriplex":
                  return "#abafa7";
              default:
                  return "gray";
          }
      }
  </script>
  
  <svg></svg>
  
  <div>
    <svg id="{svgId}"></svg>
  </div>
