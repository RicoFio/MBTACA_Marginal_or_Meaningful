<script>
    import * as d3 from 'd3';

    export let data = [];
    let arcGenerator = d3.arc().innerRadius(0).outerRadius(50);
    let sliceGenerator = d3.pie().value(d => d.value);
    let arcData;
    $: {
        arcData = sliceGenerator(data);
    }
    $: arcs = arcData.map(d => arcGenerator(d));
    export let selectedIndex = -1;

    let colors = d3.scaleOrdinal(d3.schemeTableau10);

    function toggleWedge (index, event) {
        if (!event.key || event.key === "Enter") {
            selectedIndex = selectedIndex===index?-1:index
        }
    }
</script>

<div class="chart-container">
    <svg viewBox="-50 -50 100 100">
        {#each arcs as arc, index}
            <path d={arc} fill={ colors(index) }
                  role="button"
                  tabindex="0"
                  aria-label="A clickable pie chart element"
                  class:selected={selectedIndex === index}
                  on:click={e => toggleWedge(index, e) }
                  on:keyup={e => toggleWedge(index, e)}/>
        {/each}
    </svg>

    <ul class="legend">
        {#each data as d, index}
            <li style="--color: { colors(index) }" class:selected={selectedIndex === index}>
                <span class="swatch"></span>
                {d.label} <em>( {d.value} )</em>
            </li>
        {/each}
    </ul>
</div>

<style>
    .chart-container {
        display: flex;
        align-items: center;
        gap: 10%;
    }
    .selected {
        --color: oklch(0.85 0.174 86.552) !important;
        transition: 300ms;
        &:is(path) {
            transition: 300ms;
            fill: var(--color);
        }
    }
    svg {
        max-width: 20em;
        margin-block: 2em;

        /* Do not clip shapes outside the viewBox */
        overflow: visible;
    }
    svg:has(path:hover, path:focus-visible) {
        path:not(:hover, :focus-visible) {
            opacity: 50%;
            transition: 300ms;
        }
    }

    .legend {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    path {
        /* ... */
        cursor: pointer;
        transition: 300ms;
        outline: none;
    }

    .legend li {
        display: flex;
        align-items: center;
        margin-bottom: 0.5em;
    }

    .legend .swatch {
        width: 1em;
        height: 1em;
        border-radius: 50%;
        margin-right: 0.5em;
        transition: 300ms;
        background-color: var(--color);
    }
</style>