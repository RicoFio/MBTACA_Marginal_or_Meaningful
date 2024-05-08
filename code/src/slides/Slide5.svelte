<script>
    export let active = false;
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import Treemap from "./../lib/dataVisComponents/Treemap.svelte"
    import TreemapFuture from "./../lib/dataVisComponents/TreemapFuture.svelte"
    import TreemapUsage from "./../lib/dataVisComponents/TreemapUsage.svelte"

    export let municipality = {};
    export let selectedStation = {};

    let treeMapHeight = 0;
    let treeMapUsageHeight = 0;
    let selectedComponent = 'zoning';
    let stopZoneData;
    let transformedStopZoneDataForMunicipality;
    let transformedStopZoneUsageDataForMunicipality;
    let transformedStopZoneFutureDataForMunicipality;

    let stopData = {};
    $: stopName = selectedStation?.Name;

    function transformStopZoneData(originalData) {
        let out = [
            { name: "Single Family", value: originalData[0].properties.pctZonedAsSF, category1: "pctZonedAsSF" },
            { name: "Commercial", value: originalData[0].properties.pctUsedAsCommercial, category1: "pctZonedAsComm" },
            { name: "Multi Family", value: originalData[0].properties.pctZonedAsMultifamily, category1: "pctZonedAsMultifamily" },
        ];
        console.log(out);
        return out;
    }
    function transformStopZoneUsageData(originalData) {
        let out = [
            { name: "Single Family", value: originalData[0].properties.pctUsedAsSF, category1: "pctUsedAsSF" },
            { name: "Commercial", value: originalData[0].properties.pctUsedAsCommercial, category1: "pctUsedAsCommercial" },
            { name: "Multiple Buildings on 1 Lot", value: originalData[0].properties.pctUsedAsMultiBuildings1Lot, category1: "pctUsedAsMultiBuildings1Lot" },
            { name: "Duplex", value: originalData[0].properties.pctUsedAsDuplex, category1: "pctUsedAsDuplex" },
            { name: "Triplex", value: originalData[0].properties.pctUsedAsTriplex, category1: "pctUsedAsTriplex" }
        ];
        console.log(out);
        return out;
    }
    function transformStopZoneFutureData(originalData) {
        const commercial = originalData[0].properties.pctZonedAsCommercial ?
            originalData[0].properties.pctZonedAsCommercial :
            originalData[0].properties.pctUsedAsCommercial

        let out = [
            { name: "Single Family", value: originalData[0].properties.pctFutureZonedAsSF, category1: "pctFutureZonedAsSF" },
            { name: "Commercial", value: commercial, category1: "isZonedAsCommercial" },
            { name: "Multi Family", value: originalData[0].properties.pctFutureZonedAsMulti, category1: "pctFutureZonedAsMulti" }
        ];
        return out;
    }

    onMount(async () => {
        treeMapHeight = document.getElementById('treeMap').clientHeight;
        treeMapUsageHeight = document.getElementById('treeMapUsage').clientHeight;

        stopZoneData = await d3.json(
            "/data/brookline_milton_stop_zone_zoning_usage_census_v2.geojson",
        );
    });

    $: {
        // Check the data transformation here
        stopData = stopZoneData?.features.filter(
            (feature) => feature.properties.stop_name == selectedStation?.Name,
        )

        if (stopData && stopData.length != 0) {
            transformedStopZoneDataForMunicipality = transformStopZoneData(stopData);
            transformedStopZoneUsageDataForMunicipality = transformStopZoneUsageData(stopData);
            transformedStopZoneFutureDataForMunicipality = transformStopZoneFutureData(stopData);
        }
    }

    $: treeMapVisibility = selectedComponent == 'zoning' ? 'visible' : 'hidden';
    $: treeMapUsageVisibility = selectedComponent == 'usage' ? 'visible' : 'hidden';

</script>

<div class="slide">
    {#if (municipality && selectedStation)}
        <h1>{municipality.Name}: {selectedStation.Name}</h1>
        <h3>
            The visualizations below show the area's current zoning and usage breakdown within a 0.5-mile radius of {selectedStation.Name} station. Both usage and zoning information are defined at the parcel level, and parcels within the 0.5-mile buffer are aggregated. Notice that in many areas, the zoning and usage don't necessarily match- for example, some areas zoned for multifamily development may actually have exclusively single-family dwellings currently constructed. Recall that the MBTA Communities Act does not stipulate that any current development must be changed, only that certain areas must be upzoned (and thus, there development patterns might theoretically change in the future).

            Toggle the treemap diagram to see how the current and future zoning mix differ. If a significant number of parcels around the station need to be upzoned to become compliant, this may be a big change, but in some areas, the current and future zoning mix might be very similar.
            Under the MBTA Communities Act, municipalities get to decide where to site their multifamily districts, and can use these statistics to help make their decisions. 
        </h3>
        <ul>
            <li>Parcel data, including parcel-level zoning and usage information, is sourced from</li>
            <li>Zoning code designations for Brookline from</li>
            <li>Usage code designations for the state of Massachusetts from <a href="https://cityofboston.gov" target="_blank">CityOfBoston.gov</a></li>
        </ul>
    {/if}
    <h2>WHAT'S THE HOUSING MIX?</h2>
    <div style="display: flex; align-items: center; gap: 10px;">
        <label style="cursor: pointer;">
            <input type="radio" value="zoning" bind:group={selectedComponent} />
            Zoning
        </label>
        <label style="cursor: pointer;">
            <input type="radio" value="usage" bind:group={selectedComponent} />
            Usage
        </label>
    </div>
    <br/>
    <div style="display: flex; align-items: center; gap: 10px;">
        {#key stopName}
            <div>
                {#if stopName}
                    <div style="display: flex; align-items: center; gap: 100px;">
                        <div>
                            <div id="treeMap" class={treeMapVisibility}>
                                <Treemap data={transformedStopZoneDataForMunicipality} />
                            </div>

                            <div id="treeMapUsage" class={treeMapUsageVisibility}>
                                <TreemapUsage data={transformedStopZoneUsageDataForMunicipality} />
                            </div>
                        </div>

                        <div id="treeMapFuture">
                            <TreemapFuture data={transformedStopZoneFutureDataForMunicipality} />
                        </div>
                    </div>
                {:else}
                    <p></p>
                {/if}
            </div>
        {/key}

        <div>
            <div id="treeMap" class={treeMapVisibility}>
                <h2></h2>
                {#if transformedStopZoneDataForMunicipality != undefined}

                {:else}

                {/if}
            </div>

            <div id="treeMapUsage" class={treeMapUsageVisibility}>
                <h2></h2>
                {#if transformedStopZoneUsageDataForMunicipality != undefined}

                {:else}

                {/if}
            </div>
        </div>

        <div id="treeMapFuture">

            {#if transformedStopZoneFutureDataForMunicipality != undefined}

            {:else}
            {/if}
        </div>
    </div>

    <!-- <div>
        {#if suggestions.length}
            <ul>
                {#each suggestions as suggestion}
                    <li on:click={() => selectSuggestion(suggestion)}>
                        {suggestion.Name}
                    </li>
                {/each}
            </ul>
        {/if}
    </div> -->



</div>

<style>
    .slide {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    h1 {
        font-weight: normal;
    }

    h2 {
        font-weight: normal;
    }

    h3 {
        font-weight: normal;
    }

    .hidden {
        display: none;
    }

    .visible {
        display: block;
    }

</style>
