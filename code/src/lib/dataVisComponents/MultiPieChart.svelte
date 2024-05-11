<script>
    import * as d3 from "d3";

    let width = 450;
    let height = 450;
    let margin = 40;

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    let radius = Math.min(width, height) / 2 - margin;

    // Create dummy data
    const data1 = { a: 9, b: 20, c: 30, d: 8, e: 12, f: 3, g: 7, h: 14 };
    const data2 = { a: 29, b: 2, c: 3, d: 10, e: 5, f: 3, g: 7, h: 14 };
    const data3 = { a: 20, b: 2, c: 3, d: 10, e: 5, f: 30, g: 2, h: 14 };

    // set the color scale
    const color = d3
        .scaleOrdinal()
        .domain(["a", "b", "c", "d", "e", "f", "g", "h"])
        .range(d3.schemeDark2);

    // Compute the position of each group on the pie:
    const pie = d3
        .pie()
        .sort(null) // Do not sort group by size
        .value((d) => d[1]);
    const data_ready_1 = pie(Object.entries(data1));
    const data_ready_2 = pie(Object.entries(data2));
    const data_ready_3 = pie(Object.entries(data3));

    // The arc generator
    function arc (slice, innerRadius=0.5, outerRadius=0.8) {
        return d3
            .arc()
            .innerRadius(radius * innerRadius) // This is the size of the donut hole
            .outerRadius(radius * outerRadius)(slice);
    }

    // Another arc that won't be drawn. Just for labels positioning
    const outerArc = d3
        .arc()
        .innerRadius(radius * 0.9)
        .outerRadius(radius * 0.9);
</script>

<svg
        {width}
        {height}
        viewBox="{-width / 2}, {-height / 2}, {width}, {height}"
        style:max-width="100%"
        style:height="auto"
>
    <g class="chart-inner">
        {#each data_ready_1 as slice}
            <path d={arc(slice, 0.8, 1)} fill={color(slice.data[1])} stroke="white" />
        {/each}
        {#each data_ready_2 as slice}
            <path d={arc(slice, 0.5, 0.75)} fill={color(slice.data[1])} stroke="white" />
        {/each}
        {#each data_ready_3 as slice}
            <path d={arc(slice, 0.2, 0.45)} fill={color(slice.data[1])} stroke="white" />
        {/each}
    </g>
</svg>

<style>
    :global(body) {
        margin: 0;
    }
</style>
