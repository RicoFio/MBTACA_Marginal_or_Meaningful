<script>
    import {onMount} from 'svelte';
    import * as d3 from 'd3';
    import { getCirclePackingColorByCategory } from "$lib/dataVisComponents/circlePackingUtils.js";
    import {autoPlacement, computePosition, offset} from "@floating-ui/dom";

    export let data = [];
    let svgId = 'treemap-usage-svg'; // Unique ID for the SVG
    let svg;
    let g;
    let treemapUsageTooltip;
    let tooltipPosition = {x: 0, y: 0};
    let showTooltip;
    let hoveredCircle = {};

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
            .on('mouseenter', function (event, d) {
                d3.select(this).attr('stroke', '#000');
                dotInteraction(event, d);
            })
            .on('mouseleave', function (event, d) {
                d3.select(this).attr('stroke', null);
                dotInteraction(event, d);
            });

        node.filter(d => !d.children)
            .append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '0.35em')
            .attr('fill', 'white')
            .style('font-size', '14px')
            .text(d => d.data.name);

        function createLegend() {
            const legend = d3.select('#legend-usage');

            const categories = [
                {name: 'Single Family', color: '#05515e'},
                {name: 'Duplex', color: '#999624'},
                {name: 'Triplex', color: '#999624'},
                {name: 'Commercial', color: '#97340b'}
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
    }

    async function dotInteraction(event, data) {
        let hoveredDot = event.target;
        if (event.type === "mouseenter" || event.type === "focus") {
            if (data.data.value) {
                showTooltip = true;
                hoveredCircle = {name: data.data.name, value: data.data.value.toFixed(2)};
            }
            tooltipPosition = await computePosition(hoveredDot, treemapUsageTooltip, {
                strategy: "fixed",
                middleware: [
                    offset(5),
                    autoPlacement()
                ],
            });
        } else if (event.type === "mouseleave" || event.type === "blur") {
            showTooltip = false;
        }
    }
</script>

<div>
    <svg bind:this={g} class="circle-packing"></svg>
    <div id="legend-usage" class="treemap-legend"></div>
</div>

<dl class="info"
    hidden={!showTooltip}
    style="top: {tooltipPosition.y}px; left: {tooltipPosition.x}px"
    bind:this={treemapUsageTooltip}
    role="chart-tooltip">
    <dt>{ hoveredCircle.name }</dt>
    <dd>{ hoveredCircle.value }%</dd>
</dl>

<style>
    @import "treemap.css";

    dl.info {
        z-index: 1000;
        display: grid;
        grid-template-columns: auto auto; /* Define two columns */
        grid-auto-rows: auto; /* This will create a new row for each term/description pair */
        align-items: start;
        position: fixed; /* Ensure it's positioned in relation to the SVG or a relative container */
        top: 10px;
        left: 10px;
        background-color: rgba(10, 0, 0, 0.4); /* Semi-transparent background */
        backdrop-filter: blur(10px);
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Soft shadow for better readability */
        font-size: 1.2em;
        transition-duration: 500ms;
        transition-property: opacity, visibility;
        line-height: 30px;
        padding: 10px;
        font-family: 'Montserrat', sans-serif;
        visibility: visible;
        width: 250px;
        color: #a9987a;

        &[hidden]:not(:hover, :focus-within) {
            opacity: 0;
            visibility: hidden;
        }
    }

    dl.info dt {
        font-weight: bold; /* Makes text bold */
    }
</style>