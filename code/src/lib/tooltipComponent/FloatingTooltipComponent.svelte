<script>
    import MultiPieChart from "$lib/dataVisComponents/MultiPieChart.svelte";
    import {
        loadStationZoningAndUsageData,
        loadStationZoningAndUsageDataDict
    } from "$lib/dataVisComponents/zoningData.js";

    export let stations;
    export let municipality;
    export let zoningAndCensusFiles;

    let firstStationData;
    let secondStationData;
    let firstStationInfoData;
    let secondStationInfoData;
    let loadedStation;

    $: firstStation = (stations?.length > 0) ? stations[0] : undefined;
    $: secondStation = (stations?.length > 1) ? stations[1] : undefined;

    $: firstStation, (async () => {
        if (firstStation !== undefined && firstStation?.Name !== loadedStation?.Name) {
            firstStationData = await loadStationZoningAndUsageData(zoningAndCensusFiles, firstStation);
            firstStationInfoData = await loadStationZoningAndUsageDataDict(zoningAndCensusFiles, firstStation);
        }
    })();

    $: secondStation, (async () => {
        if (secondStation !== undefined && secondStation?.Name !== loadedStation?.Name) {
            secondStationData = await loadStationZoningAndUsageData(zoningAndCensusFiles, secondStation);
            secondStationInfoData = await loadStationZoningAndUsageDataDict(zoningAndCensusFiles, secondStation);
        }
    })();

</script>

<div class="floating-panel">
    <h1>Municipality <b>{ municipality?.Name }</b></h1>
    <div class="station-panel-container">
        <h2><b>{ firstStation?.Name }</b></h2>
        <MultiPieChart bind:stationData={firstStationData}/>
        <p>{ String(firstStationInfoData?.pctMustUpzone).slice(0, 5) }% of parcels <b>must upzone</b></p>
        <p>{ String(firstStationInfoData?.pctWillChange).slice(0, 5) }% of parcels <b>must change</b></p>
    </div>
    <div class="station-panel-container">
        <h2><b>{ secondStation?.Name }</b></h2>
        <MultiPieChart bind:stationData={secondStationData}/>
        <p>{ String(secondStationInfoData?.pctMustUpzone).slice(0, 5) }% of parcels <b>must upzone</b></p>
        <p>{ String(secondStationInfoData?.pctWillChange).slice(0, 5) }% of parcels <b>must change</b></p>
    </div>
</div>

<style>
    .floating-panel {
        position: fixed;
        left: 5%;
        top: 50%; /* Center the panel vertically */
        transform: translateY(-50%);
        width: 380px; /* Adjust the width as necessary */
        background: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        border-radius: 5px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        z-index: 1000; /* Make sure it floats above other content */
        grid-template-columns: auto auto; /* Define two columns */
        grid-auto-rows: auto; /* This will create a new row for each term/description pair */
        /*align-items: start;*/
        background-color: rgba(10, 0, 0, 0.4); /* Semi-transparent background */
        backdrop-filter: blur(10px);
        font-size: 0.9em;
        transition-duration: 500ms;
        transition-property: opacity, visibility;
        gap: 0px;
        justify-content: center;
        font-family: 'Montserrat', sans-serif;
        visibility: visible;
        color: #a9987a;
        line-height: 5px;
        align-items: center;
    }

    .station-panel-container {
        align-items: center;
    }

    .graph {
        height: 200px; /* Adjust based on your needs */
        background-color: #f0f0f0; /* A light grey background to distinguish the graph area */
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #ccc; /* Optional border for graph boxes */
    }
</style>
