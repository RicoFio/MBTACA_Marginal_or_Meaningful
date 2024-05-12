<script>
    import {onMount} from 'svelte';
    import * as d3 from 'd3';
    import { getCirclePackingColorByCategory } from "$lib/dataVisComponents/circlePackingUtils.js";

    export let data = [];
    let svgId = 'treemap-usage-svg'; // Unique ID for the SVG
    let svg, tooltip;
    let g;

    onMount(() => {
        if (data && data.length > 0) {
            drawCirclePacking();
        }
    });

    function drawCirclePacking() {
        const width = 400;
        const height = 400;

        svg = d3.select(g)
            .attr('viewBox', `0 0 ${width} ${height}`)
            .attr('width', width)
            .attr('height', height)
            .style('display', 'block')
            .style('margin', '0 auto');

        tooltip = d3.select('#tooltip-usage');

        const root = d3.hierarchy({name: 'root', children: data})
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);

        const pack = d3.pack()
            .size([width, height])
            .padding(3);

        pack(root);

        const nodes = root.descendants();
        createLegend();
        const node = svg.selectAll('g')
            .data(nodes)
            .join('g')
            .attr('transform', d => `translate(${d.x}, ${d.y})`);

        node.append('circle')
            .attr('r', d => d.r)
            .attr('fill', d => d.children ? '#9f9090' : getCirclePackingColorByCategory(d.data))
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
            const legend = d3.select('#legend-usage');

            const categories = [
                {name: 'Single Family', color: '#05515e'},
                {name: 'Duplex', color: '#629681'},
                {name: 'Triplex', color: '#97340b'},
                {name: 'Commercial', color: '#abafa7'}
            ];

            legend.selectAll('legend-usage')
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
                case 'pctUsedAsSF':
                    return '#05515e';
                case 'pctUsedAsCommerical':
                    return '#abafa7';
                case 'pctUsedAsDuplex':
                    return '#629681';
                case 'pctUsedAsTriplex':
                    return '#97340b';
                default:
                    return 'gray';
            }
        }
    }
</script>

<div id="tooltip" class="treemap-tooltip"></div>

<div>
    <svg bind:this={g} class="circle-packing"></svg>
    <div id="legend-usage" class="treemap-legend"></div>
</div>

<style>
    @import "treemap.css";
</style>