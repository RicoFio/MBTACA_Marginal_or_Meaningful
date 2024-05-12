<script>
    import MultiPieChart from "$lib/dataVisComponents/MultiPieChart.svelte";
    import {loadStationZoningAndUsageData} from "$lib/dataVisComponents/zoningData.js";

    export let active = false;

    export let municipality = {};
    export let station = {};
    export let zoningAndCensusFiles = {};

    let stationData = {};

    $: {
        if (station) {
            stationData = loadStationZoningAndUsageData(zoningAndCensusFiles, station);
        }
    }
</script>

<div class="slide">
    <div style="display: flex; align-items: center; gap: 10px;">
        <h1>LETS TALK</h1>
        {#key station}
            <h2>ABOUT THIS</h2>
            {#if station}
                <MultiPieChart bind:stationData={stationData} />
            {:else}

            {/if}
        {/key}
    </div>
</div>

<style>
    @import url("$lib/slide.css");

    .hidden {
        display: none;
    }

    .visible {
        display: block;
    }
</style>
