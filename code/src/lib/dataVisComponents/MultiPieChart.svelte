<script>
    import * as d3 from "d3";
    import {autoPlacement, computePosition, offset} from "@floating-ui/dom";

    let width = 450;
    let height = 450;
    let margin = 40;

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
        .scaleOrdinal()
        .domain(["singleFamily", "commercial", "multiFamily"])
        .range(d3.schemeDark2);

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

    let donutTooltip, showTooltip, tooltipPosition;
    let hoveredSlice;

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
</script>

{#key stationData}
    <svg
            {width}
            {height}
            viewBox="{-width / 2}, {-height / 2}, {width}, {height}"
            style:max-width="100%"
            style:height="auto"
    >
        <g class="chart-inner">
            {#each zoning_pie_data as slice, index}
                {console.log("&&&&&&&&&&&&")}
                {console.log(slice.data[0])}
                {console.log("&&&&&&&&&&&&")}
                <path d={arc(slice, 0.8, 1)} fill={color(slice.data[0])} stroke="white"
                      on:mouseenter={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:mouseleave={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:focus={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:blur={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:click={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:keyup={(evt) => dotInteraction(slice.data[1], index, evt)}
                />
            {/each}
            {#each usage_pie_data as slice, index}
                <path d={arc(slice, 0.5, 0.75)} fill={color(slice.data[1])} stroke="white"
                      on:mouseenter={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:mouseleave={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:focus={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:blur={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:click={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:keyup={(evt) => dotInteraction(slice.data[1], index, evt)}
                />
            {/each}
            {#each future_pie_data as slice, index}
                <path d={arc(slice, 0.2, 0.45)} fill={color(slice.data[1])} stroke="white"
                      on:mouseenter={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:mouseleave={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:focus={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:blur={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:click={(evt) => dotInteraction(slice.data[1], index, evt)}
                      on:keyup={(evt) => dotInteraction(slice.data[1], index, evt)}
                />
            {/each}
        </g>
    </svg>
{/key}

<dl class="info"
    hidden={!showTooltip}
    style="top: {tooltipPosition.y}px; left: {tooltipPosition.x}px"
    bind:this={donutTooltip}
    role="tooltip">
    <dt>{ hoveredSlice.name }</dt>
    <dd>{ hoveredSlice.value }</dd>
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
        gap: 0.5em; /* Adjust the gap between items */
        align-items: start;
        position: fixed; /* Ensure it's positioned in relation to the SVG or a relative container */
        top: 10px;
        left: 10px;
        background-color: rgba(10, 0, 0, 0.4); /* Semi-transparent background */
        backdrop-filter: blur(10px);
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Soft shadow for better readability */
        font-size: 0.9em;
        padding: 1em;
        transition-duration: 500ms;
        transition-property: opacity, visibility;

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
