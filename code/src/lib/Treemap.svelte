<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let data = [];

  let svg, tooltip;

  onMount(() => {
    if (data && data.length > 0) {
      drawCirclePacking();
    }
  });

  function drawCirclePacking() {
    
    const width = 400;
    const height = 400;

    svg = d3.select('svg')
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('width', width)
      .attr('height', height)
      .style('display', 'block')
      .style('margin', '0 auto');

    tooltip = d3.select('#tooltip');

    const root = d3.hierarchy({ name: 'root', children: data })
      .sum(d => d.value)
      .sort((a, b) => b.value - a.value);

    const pack = d3.pack()
      .size([width, height])
      .padding(3);

    pack(root);

    const zoom = d3.zoom()
      .scaleExtent([1, 8])
      .on('zoom', event => {
        svg.attr('transform', event.transform);
      });

    svg.call(zoom);

    const nodes = root.descendants();
    createLegend();
    const node = svg.selectAll('g')
      .data(nodes)
      .join('g')
      .attr('transform', d => `translate(${d.x}, ${d.y})`);

    node.append('circle')
      .attr('r', d => d.r)
      .attr('fill', d => d.children ? '#abafa7' : getColorByCategory(d.data))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .on('mouseover', function (event, d) {
        d3.select(this).attr('stroke', '#000');
        showTooltip(event, d);
      })
      .on('mouseout', function () {
        d3.select(this).attr('stroke', '#fff');
        hideTooltip();
      });

    node.filter(d => !d.children)
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', 'white')
      .style('font-size', '14px')
      .text(d => d.data.name);

    function getColorByCategory(d) {
      return d.category1 === 'pctZonedAsSF' ? '#dd8155' :
             d.category1 === 'pctZonedAsComm' ? '#05515e' :
             d.category1 === 'pctZonedAsMultifamily' ? '#97340b' :
             'gray';
    }

    

    function showTooltip(event, d) {
      tooltip.style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px')
        .style('display', 'inline-block')
        .html(`<strong>${d.data.name}</strong><br>Value: ${d.value}`);
    }

    function hideTooltip() {
      tooltip.style('display', 'none');
    }

    function createLegend() {
      const legend = d3.select('#legend-main');

      const categories = [
        { name: 'Single Family', color: '#dd8155' },
        { name: 'Commercial', color: '#05515e' },
        { name: 'Multi Family', color: '#97340b' }
      ];

      legend.selectAll('div')
        .data(categories)
        .enter()
        .append('div')
        .style('display', 'flex')
        .style('align-items', 'center')
        .style('margin-bottom', '4px')
        .html(d => `
          <span style="display: inline-block; width: 15px; height: 15px; background: ${d.color}; margin-right: 8px;"></span>
          ${d.name}
        `);
    }
  }
</script>

<div id="tooltip" style="position: absolute; display: none; background: lightsteelblue; padding: 5px; border-radius: 3px; pointer-events: none; font: 12px sans-serif;"></div>

<svg bind:this={svg} width=400 height=400></svg>
<div id="legend-main"></div>

<style>
  circle {
    fill-opacity: 0.6;
    transition: fill-opacity 0.3s, stroke-width 0.3s;
  }
  circle:hover {
    fill-opacity: 50;
    stroke-width: 3px;
  }
  text {
    pointer-events: none;
  }
  #legend-main {
    margin: 10px auto;
    width: 200px;
  }
</style>