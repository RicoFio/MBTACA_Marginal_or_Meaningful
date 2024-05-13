<script>
    import * as d3 from "d3";
    import {autoPlacement, computePosition, offset} from "@floating-ui/dom";

    let width = 280;
    let height = 280;
    let margin = 35;

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    let radius = Math.min(width, height) / 2 - margin;
    let zoning_pie_data;
    let usage_pie_data;
    let future_pie_data;

    // Create dummy data
    export let stationData = undefined;

    $: {
        if (stationData !== undefined) {
            let zoningData = stationData.currentZoning;
            let usageData = stationData.currentUsage;
            let futureZoningData = stationData.futureZoning;
            zoning_pie_data = pie(Object.entries(zoningData));
            usage_pie_data = pie(Object.entries(usageData));
            future_pie_data = pie(Object.entries(futureZoningData));
        }
    }

    // set the color scale
    const color = d3
        .scaleOrdinal(['#f39034', '#97340b', '#999624', '#abafa7'])
        .domain(["singleFamily", "commercial", "multiFamily", "other"]);

    // Compute the position of each group on the pie:
    const pie = d3
        .pie()
        .sort(null) // Do not sort group by size
        .value((d) => d[1].value);

    // The arc generator
    function arc(slice, innerRadius, outerRadius) {
        return d3
            .arc()
            .innerRadius(radius * innerRadius) // This is the size of the donut hole
            .outerRadius(radius * outerRadius)(slice);
    }

    let donutTooltip, showTooltip;
    let tooltipPosition = {x: 0, y: 0};
    let hoveredSlice = {};

    async function dotInteraction(data, index, event) {
        let hoveredDot = event.target;
        if (event.type === "mouseenter" || event.type === "focus") {
            // dot hovered
            // cursor = {x: evt.x, y: evt.y};
            showTooltip = true;
            tooltipPosition = await computePosition(hoveredDot, donutTooltip, {
                strategy: "fixed", // because we use position: fixed
                middleware: [
                    offset(5), // spacing from tooltipComponent to dot
                    autoPlacement() // see https://floating-ui.com/docs/autoplacement
                ],
            });
            hoveredSlice = {name: data.name, value: data.value.toFixed(2)};
        } else if (event.type === "mouseleave" || event.type === "blur") {
            showTooltip = false;
        }
    }

    const idContainer = Math.random() * 100;
</script>

{#key stationData}
    <svg
            {width}
            {height}
            viewBox="{-width / 2 - 20}, {-height / 2 - 20}, {width + 50}, {height + 50}"
            style:max-width="100%"
            style:height="auto"
    >
        <g class="chart-inner">
            {#each zoning_pie_data as slice, index}
                <path d={arc(slice, 0.2, 0.4)} fill={color(slice.data[0])} stroke="white" stroke-width="3"
                      on:mouseenter={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:mouseleave={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:focus={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:blur={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:click={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:keyup={(evt) => dotInteraction(slice.data[1], index, evt)}
                />
            {/each}
            {#each usage_pie_data as slice, index}
                <path d={arc(slice, 0.65, 0.85)} fill={color(slice.data[0])} stroke="white" stroke-width="3"
                      on:mouseenter={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:mouseleave={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:focus={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:blur={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:click={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:keyup={(evt) => dotInteraction(slice.data[1], index, evt)}
                />
            {/each}
            {#each future_pie_data as slice, index}
                <path d={arc(slice, 1.12, 1.34)} fill={color(slice.data[0])} stroke="white" stroke-width="3"
                      on:mouseenter={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:mouseleave={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:focus={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:blur={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:click={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:keyup={(evt) => dotInteraction(slice.data[1], index, evt)}
                />
            {/each}
        </g>
        <path id={`wavy-current-zoning-${idContainer}`} d={arc({startAngle: 0, endAngle:5.8, padAngle: 0}, 0.2, 0.48)}
              class="donut-text-path" transform='rotate(95)'></path>
        <text style="text-anchor: middle;">
            <textPath xlink:href={`#wavy-current-zoning-${idContainer}`} startOffset="50%" class="donut-text">
                Current Zoning
            </textPath>
        </text>
        <path id={`wavy-current-usage-${idContainer}`} d={arc({startAngle: 0, endAngle:5.8, padAngle: 0}, 0.2, 0.92)}
              class="donut-text-path" transform='rotate(114)'></path>
        <text style="text-anchor: middle;">
            <textPath xlink:href={`#wavy-current-usage-${idContainer}`} startOffset="50%" class="donut-text">
                Current Usage
            </textPath>
        </text>
        <path id={`wavy-future-${idContainer}`} d={arc({startAngle: 0, endAngle:5.8, padAngle: 0}, 0.2, 1.4)}
              class="donut-text-path" transform='rotate(120)'></path>
        <text style="text-anchor: middle;">
            <textPath xlink:href={`#wavy-future-${idContainer}`} startOffset="50%" class="donut-text">
                Future Zoning
            </textPath>
        </text>
    </svg>
{/key}

<dl class="info"
    hidden={!showTooltip}
    style="top: {tooltipPosition.y}px; left: {tooltipPosition.x}px"
    bind:this={donutTooltip}
    role="chart-tooltip">
    <dt>{ hoveredSlice.name }</dt>
    <dd>{ hoveredSlice.value }%</dd>
</dl>

<style>
    :global(body) {
        margin: 0;
    }

    dl.info {
        z-index: 2;
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
        width: 400px;
        color: #a9987a;

        &[hidden]:not(:hover, :focus-within) {
            opacity: 0;
            visibility: hidden;
        }
    }

    .donut-text-path {
        fill: none;
    }

    .donut-text {
        fill: #f0f0f0;
        font-weight: bold;
    }

    dl.info dt {
        font-weight: bold; /* Makes text bold */
    }
</style>
