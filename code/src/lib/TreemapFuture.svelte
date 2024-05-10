<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let data = [];
  let svgId = 'treemap-future-svg'; // Unique ID for the SVG
  let svg, tooltip;

  onMount(() => {
    if (data && data.length > 0) {
      drawCirclePacking();
    }
  });

  function drawCirclePacking() {
    const width = 400;
    const height = 400;

    svg = d3.select(`#${svgId}`)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('width', width)
      .attr('height', height)
      .style('display', 'block')
      .style('margin', '0 auto');

    tooltip = d3.select('#tooltip-future');

    const root = d3.hierarchy({ name: 'root', children: data })
      .sum(d => d.value)
      .sort((a, b) => b.value - a.value);

    const pack = d3.pack()
      .size([width, height])
      .padding(3);

    pack(root);

    const nodes = root.descendants();

    const node = svg.selectAll('g')
      .data(nodes)
      .join('g')
      .attr('transform', d => `translate(${d.x}, ${d.y})`);

    node.append('circle')
      .attr('r', d => d.r)
      .attr('fill', d => d.children ? '#bbb' : getColorByCategory(d.data))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .on('mouseover', function (event, d) {
        d3.select(this).attr('stroke', '#000');
        showTooltip(event, d);
      })
      .on('mouseout', function () {
        d3.select(this).attr('stroke', null);
        hideTooltip();
      });

    node.filter(d => !d.children)
      .append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', 'white')
      .style('font-size', '14px')
      .text(d => d.data.name);

    createLegend();

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
      const legend = d3.select('#legend-future');

      const categories = [
        { name: 'Future Single Family', color: '#999624' },
        { name: 'Commercial', color: '#3e5719' },
        { name: 'Future Multi Family', color: '#05515e' }
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

    function getColorByCategory(d) {
      switch (d.category1) {
        case 'pctFutureZonedAsSF':
          return '#999624';
        case 'isZonedAsCommercial':
          return '#3e5719';
        case 'pctFutureZonedAsMulti':
          return '#05515e';
        default:
          return 'gray';
      }
    }
  }
</script>

<div id="tooltip-future" style="position: absolute; display: none; background: lightsteelblue; padding: 5px; border-radius: 3px; pointer-events: none; font: 12px sans-serif;"></div>
<svg id="{svgId}"></svg>
<div id="legend-future"></div>

<style>
  circle {
    fill-opacity: 0.6;
    transition: fill-opacity 0.3s, stroke-width 0.3s;
  }
  circle:hover {
    fill-opacity: 1;
    stroke-width: 3px;
  }
  text {
    pointer-events: none;
  }
  #legend-future {
    margin: 10px auto;
    width: 200px;
  }
</style>
