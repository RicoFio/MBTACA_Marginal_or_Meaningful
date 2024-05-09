<!-- TreemapUsage.svelte -->

<script>
  import {onMount} from "svelte";
  import * as d3 from "d3";
  import {getTreemapColorByCategory} from "$lib/dataVisComponents/treemapUtils.js";

  export let data = [];
  let svgId = 'treemap-usage-svg'; // Unique ID for the SVG

  function drawTreemap() {
      const width = 400;
      const height = 250;
      const svg = d3
          .select(`#${svgId}`) // Use the unique ID for selection
          .attr("width", width)
          .attr("height", height);
      // Transform data into hierarchy
      const root = d3.hierarchy({children: data}).sum((d) => d.value);
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
          .attr("fill", (d) => getTreemapColorByCategory(d.data))
          .on("mouseover", handleMouseOver)
          .on("mouseout", handleMouseOut);
      cell.append("title")
          .text((d) => d.data.name);
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
          d3.select(this).attr("fill", (d) => getTreemapColorByCategory(d.data));
      }
  }

  onMount(() => {
    if (data.length > 0) drawTreemap();
  });

  $: if (data.length > 0) {
    drawTreemap();
  }
</script>

<div>
  <svg id={svgId}></svg>
</div>
