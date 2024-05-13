<script>
    import MultiPieChart from "$lib/dataVisComponents/MultiPieChart.svelte";
    import {loadStationZoningAndUsageData} from "$lib/dataVisComponents/zoningData.js";

    export let active = false;

    export let municipality = {};
    export let station;
    let loadedStation;
    export let zoningAndCensusFiles = {};

    let stationData;

    $: station, (async () => {
        if (station !== undefined && station?.Name !== loadedStation?.Name) {
            stationData = await loadStationZoningAndUsageData(zoningAndCensusFiles, station);
        }
    })();
</script>

<div class="slide">
    <div style="display: flex; align-items: center; gap: 10px;">
        {#key station}
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
