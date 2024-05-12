<script>
    import MultiPieChart from "$lib/dataVisComponents/MultiPieChart.svelte";

    export let active = false;
    import {transformStopZoneData, transformStopZoneUsageData, transformStopZoneFutureData} from "$lib/dataVisComponents/zoningData.js";

    export let municipality = {};
    export let station = {};

    let stopData = {};
    let transformedZoning;
    let transformedUsage;
    let transformedFuture;
    $: stopName = station?.Name;

    $: {
        // Check the data transformation here
        stopData = stopZoneData?.features.filter(
            (feature) => feature.properties.stop_name == stopName,
        )
        if (stopData) {
            transformedZoning = transformStopZoneData(stopData);
            transformedUsage = transformStopZoneUsageData(stopData);
            transformedFuture = transformStopZoneFutureData(stopData);
        }
    }
</script>

<div class="slide">
    <div style="display: flex; align-items: center; gap: 10px;">
        {#key stopName}
            {#if stopName}
                < MultiPieChart bind:zoningData={transformedZoning} bind:usageData={transformedUsage} bind:futureZoningData={transformedFuture} />
            {:else}
                <p></p>
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
