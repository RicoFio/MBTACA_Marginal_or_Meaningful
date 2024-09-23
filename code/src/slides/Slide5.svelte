<script>
    export let active = false;
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import Treemap from "./../lib/dataVisComponents/Treemap.svelte";
    import TreemapFuture from "./../lib/dataVisComponents/TreemapFuture.svelte";
    import TreemapUsage from "./../lib/dataVisComponents/TreemapUsage.svelte";

    export let municipality = {};
    export let station = {};

    let selectedComponent = "zoning";
    let stopZoneData;
    let transformedStopZoneDataForMunicipality;
    let transformedStopZoneUsageDataForMunicipality;
    let transformedStopZoneFutureDataForMunicipality;

    let stopData = [];
    $: stopName = station?.Name;

    function transformStopZoneData(originalData) {
        let out = [
            {
                name: "Single Family",
                value: originalData[0].properties.pctZonedAsSF,
                category1: "pctZonedAsSF",
            },
            {
                name: "Commercial",
                value: originalData[0].properties.pctUsedAsCommercial,
                category1: "pctZonedAsComm",
            },
            {
                name: "Multi Family",
                value: originalData[0].properties.pctZonedAsMultifamily,
                category1: "pctZonedAsMultifamily",
            },
        ];
        return out;
    }

    function transformStopZoneUsageData(originalData) {
        let out = [
            {
                name: "Single Family",
                value: originalData[0].properties.pctUsedAsSF,
                category1: "pctUsedAsSF",
            },
            {
                name: "Commercial",
                value: originalData[0].properties.pctUsedAsCommercial,
                category1: "pctUsedAsCommercial",
            },
            {
                name: "Duplex",
                value: originalData[0].properties.pctUsedAsDuplex,
                category1: "pctUsedAsDuplex",
            },
            {
                name: "Triplex",
                value: originalData[0].properties.pctUsedAsTriplex,
                category1: "pctUsedAsTriplex",
            },
        ];
        return out;
    }

    function transformStopZoneFutureData(originalData) {
        const commercial = originalData[0].properties.pctZonedAsCommercial
            ? originalData[0].properties.pctZonedAsCommercial
            : originalData[0].properties.pctUsedAsCommercial;

        let out = [
            {
                name: "Commercial",
                value: commercial,
                category1: "isZonedAsCommercial",
            },
            {
                name: "Multi Family",
                value: originalData[0].properties.pctFutureZonedAsMulti,
                category1: "pctFutureZonedAsMulti",
            },
        ];
        return out;
    }

    onMount(async () => {
        stopZoneData = await d3.json(
            "/data/all_municipalities_stop_zone_zoning_usage_census_v2.geojson",
        );
    });

    $: {
        // Check the data transformation here
        stopData = stopZoneData?.features.filter(
            (feature) => feature.properties.stop_name == stopName,
        );
        if (stopData && stopData.length != 0) {
            transformedStopZoneDataForMunicipality =
                transformStopZoneData(stopData);
            transformedStopZoneUsageDataForMunicipality =
                transformStopZoneUsageData(stopData);
            transformedStopZoneFutureDataForMunicipality =
                transformStopZoneFutureData(stopData);
        }
    }

    $: treeMapVisibility = activeSelection == "zoning" ? "visible" : "hidden";
    $: treeMapUsageVisibility =
        activeSelection == "usage" ? "visible" : "hidden";
    let activeSelection = "zoning";

    function isSelected(value) {
        return activeSelection === value ? "selected" : "";
    }
</script>

<div class="slide">
    {#if municipality && station}
        <h1>{municipality.Name}: {station.Name}</h1>
        <p>
            The visualizations below show the area's current zoning and usage
            breakdown within a 0.5-mile radius of {station.Name} station. Both usage
            and zoning information are defined at the parcel level, and parcels within
            the 0.5-mile buffer are aggregated. Notice that in many areas, the zoning
            and usage don't necessarily match- for example, some areas zoned for
            multifamily development may actually have exclusively single-family dwellings
            currently constructed. Recall that the MBTA Communities Act does not
            stipulate that any current development must be changed, only that certain
            areas must be upzoned (and thus, there development patterns might theoretically
            change in the future). Toggle the treemap diagram to see how the current
            and future zoning mix differ. If a significant number of parcels around
            the station need to be upzoned to become compliant, this may be a big
            change, but in some areas, the current and future zoning mix might be
            very similar. Under the MBTA Communities Act, municipalities get to decide
            where to site their multifamily districts, and can use these statistics
            to help make their decisions.
        </p>
    {/if}
    <h2>WHAT'S THE HOUSING MIX?</h2>
    <div class="treemap-container">
        {#key stopName}
            <div>
                {#if stopName}
                    <div class="radio-container">
                        {#each ["zoning", "usage"] as category}
                            <label class={isSelected(category)}>
                                <input
                                    type="radio"
                                    bind:group={activeSelection}
                                    name="selector"
                                    value={category}
                                />
                                {category.replace(/_/g, " ").toUpperCase()}
                                <!-- Improved readability -->
                            </label>
                        {/each}
                    </div>
                    <br />
                    <div
                        style="display: flex; align-items: center; gap: 100px;"
                    >
                        <div>
                            <div id="treeMap" class={treeMapVisibility}>
                                <Treemap
                                    data={transformedStopZoneDataForMunicipality}
                                />
                            </div>

                            <div
                                id="treeMapUsage"
                                class={treeMapUsageVisibility}
                            >
                                <TreemapUsage
                                    data={transformedStopZoneUsageDataForMunicipality}
                                />
                            </div>
                        </div>

                        <div id="treeMapFuture">
                            <TreemapFuture
                                data={transformedStopZoneFutureDataForMunicipality}
                            />
                        </div>
                    </div>
                {:else}
                    <p></p>
                {/if}
            </div>
        {/key}
    </div>
    <div>
        {#if stopData?.length > 0}
            <p>
                In the area surrounding {stopName}, there are currently {String(
                    stopData[0].properties.pctZonedAsSF,
                ).slice(0, 5)}% parcels zoned for single family residency, of
                which {String(stopData[0].properties.pctUsedAsSF).slice(0, 5)}%
                are actually used as Single Family. This means that
                {String(stopData[0].properties.pctMustUpzone).slice(0, 5)}%
                parcels (colored in orange in the map on the right) must upzone
                in order to comply with the MBTA communities Act, and
                {String(stopData[0].properties.pctWillChange).slice(0, 5)}% will
                likely actually change their use. The parcels in green, in turn,
                do not have to change.
            </p>
            <p>
                Should you see parcels in white on the right, it means that we
                have not yet processed the data for this station.
            </p>
        {/if}
    </div>
</div>
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />

<style>
    @import url("$lib/slide.css");

    .hidden {
        display: none;
    }

    .visible {
        display: block;
    }

    .radio-container {
        position: relative;
        top: 16px;
        left: 16px;
        padding: 4px;
        border-radius: 2px;
        display: flex;
        flex-direction: row; /* Align items horizontally */
        gap: 10px; /* Add some space between items */
    }

    /* Basic styling for labels */
    label {
        cursor: pointer;
        transition: font-weight 0.3s ease;
        white-space: nowrap; /* Prevent labels from wrapping */
    }

    /* Hide the radio button */
    input[type="radio"] {
        display: none;
    }

    /* When a label is selected, make the text bold */
    .selected {
        font-weight: bold;
    }

    .treemap-container {
        display: flex;
        width: 100%; /* Ensures it takes up no more than 100% of its parent */
        max-width: 100%; /* Ensures it does not exceed the width of the parent */
        flex-wrap: wrap; /* Ensures contents wrap and do not overflow */
        align-items: center;
        gap: 10px;
    }
</style>
