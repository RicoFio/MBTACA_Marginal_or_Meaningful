<script>
    export let active = false;
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import Treemap from "./../lib/dataVisComponents/Treemap.svelte"
    import TreemapFuture from "./../lib/dataVisComponents/TreemapFuture.svelte"
    import TreemapUsage from "./../lib/dataVisComponents/TreemapUsage.svelte"

    export let municipality = {};
    export let selectedStation = {};

    let mapHeight = 0;
    let treeMapHeight = 0;
    let treeMapUsageHeight = 0;
    let treeMapFutureHeight = 0;
    let selectedComponent = 'zoning'; // Start with no component selected
    let suggestions = [];
    let stopZoneData;
    // let brooklineStopZoneData;
    // let coolidgeCornerStopZoneData;
    let transformedStopZoneDataForMunicipality;
    let transformedStopZoneUsageDataForMunicipality;
    let transformedStopZoneFutureDataForMunicipality;
    let parcelData;
    let treeMapHeaderText;
    let treeMapUsageHeaderText;
    let treeMapFutureHeaderText;

    onMount(async () => {
        // treeMapHeight = document.getElementById('treeMap').clientHeight;
        // treeMapUsageHeight = document.getElementById('treeMapUsage').clientHeight;

        //console.log("treeMapUsageHeight:", treeMapUsageHeight);

        // Calculate the total height required
        // const totalHeight = (mapHeight + treeMapHeight)*4;

        // Set the body height to accommodate both components

        function transformStopZoneData(originalData) {
            return [
                { name: "Single Family Zoning", value: originalData[0].properties.pctZonedAsSF, category1: "pctZonedAsSF" },
                { name: "Commerical Zoning", value: originalData[0].properties.pctZonedAsComm, category1: "pctZonedAsComm" },
                { name: "MultiFamily Zoning", value: originalData[0].properties.pctZonedAsMulti, category1: "pctZonedAsMulti" },
            ];
        }

        function transformStopZoneUsageData(originalData) {
            return [
                { name: "Single Family Usage", value: originalData[0].properties.pctUsedAsSF, category1: "pctUsedAsSF" },
                { name: "Commerical Usage", value: originalData[0].properties.pctUsedAsComm, category1: "pctUsedAsComm" },
                { name: "Multi Family Usage", value: originalData[0].properties.pctUsedAsMulti, category1: "pctUsedAsMulti" },
                { name: "Duplex Usage", value: originalData[0].properties.pctUsedAsDuplex, category1: "pctUsedAsDuplex" },
                { name: "Triplex Usage", value: originalData[0].properties.pctUsedAsTriplex, category1: "pctUsedAsTriplex" }
            ];
        }

        function transformStopZoneFutureData(originalData) {
            return [
                { name: "Asian", value: originalData[0].properties.pctNhAsian, category1: "pctNhAsian" },
                { name: "Black", value: originalData[0].properties.pctNhBlack, category1: "pctNhBlack" },
                { name: "White", value: originalData[0].properties.pctNhWhite, category1: "pctNhWhite" },
                { name: "Hispanic", value: originalData[0].properties.pctHispanic, category1: "pctHispanic" }
            ];
        }

        // municipalities = await d3.json("/data/mbta_municipalities.geojson");
        // stations = await d3.json("/data/mbta_community_stops.geojson");

        stopZoneData = await d3.json(
            "/data/brookline_milton_stop_zone_dummies.geojson"
        );
        let brooklineStopZoneData = stopZoneData.features.filter(
            (feature) => feature.properties.community === "Brookline",
        );

        let coolidgeCornerStopZoneData = stopZoneData.features.filter(
            (feature) => feature.properties.stop_name === "Coolidge Corner",
        );
        transformedStopZoneDataForMunicipality = [
            { name: "Single Family Zoning", value: coolidgeCornerStopZoneData[0].properties.pctZonedAsSF, category1: "pctZonedAsSF" },
            { name: "Commerical Zoning", value: coolidgeCornerStopZoneData[0].properties.pctZonedAsComm, category1: "pctZonedAsComm" },
            { name: "MultiFamily Zoning", value: coolidgeCornerStopZoneData[0].properties.pctZonedAsMulti, category1: "pctZonedAsMulti" },
        ];

        transformedStopZoneUsageDataForMunicipality = transformStopZoneUsageData(
            coolidgeCornerStopZoneData,
        );

        transformedStopZoneFutureDataForMunicipality = transformStopZoneFutureData(
            coolidgeCornerStopZoneData,
        );

        parcelData = await d3.json(
            "/data/brookline_milton_parcels_dummies.geojson",
        );


        //     municipalities = municipalities.features.map((municipality) => {
        //         let newMunicipality = {};
        //         newMunicipality.PolygonCoordinates = [];

        //         if (
        //             municipality.geometry &&
        //             Array.isArray(municipality.geometry.coordinates[0])
        //         ) {
        //             newMunicipality.PolygonCoordinates =
        //                 municipality.geometry.coordinates[0];
        //         } else {
        //             console.log(municipality);
        //         }
        //         newMunicipality.Name = municipality.properties.community;
        //         newMunicipality.TotalHousingUnits =
        //             municipality.properties.housing_units_2020;
        //         newMunicipality.PopulationSize = municipality.properties.pop2020;
        //         newMunicipality.MBTACommunityType =
        //             municipality.properties.mbta_comm_type;
        //         newMunicipality.MinHousingCapacityRequirement =
        //             municipality.properties.min_rf1_cap_req;
        //         return newMunicipality;
        //     });//
    });

    // Reactive statement to update suggestions based on input
    // $: if (input) {
    //     suggestions = municipalities.filter(
    //         (m) =>
    //             m.Name &&
    //             typeof m.Name === "string" &&
    //             m.Name.toLowerCase().startsWith(input.toLowerCase()),
    //     );
    // } else {
    //     suggestions = [];
    // }

    // $: treeMapVisibility = selectedComponent === 'zoning' ? 'visible' : 'hidden';
    // $: treeMapUsageVisibility = selectedComponent === 'usage' ? 'visible' : 'hidden';


    // function selectSuggestion(suggestion) {
    //     query = suggestion.Name; // Set the query to the selected municipality name
    //     suggestions = []; // Clear suggestions

    //     // Calculate the bounding box of the selected municipality
    //     const bounds = calculateBoundingBox(suggestion.PolygonCoordinates);

    //     treeMapHeaderText = `Zoning Breakdown for: ${suggestion.Name}`
    //     treeMapUsageHeaderText = `Usage Breakdown for: ${suggestion.Name}`

    //     // Update the map view to fit the bounding box with some padding
    //     // map.fitBounds(bounds, { padding: 20 });
    // }

    // function projectPolygonCoordinates(coordinates) {
    //     return coordinates
    //         .map((coord) => {
    //             let { cx, cy } = getCoords({ Lat: coord[1], Long: coord[0] });
    //             return `${cx},${cy}`;
    //         })
    //         .join(" ");
    // }

    // function getCoords(station) {
    //     const longitude = parseFloat(station.Long);
    //     const latitude = parseFloat(station.Lat);

    //     if (isNaN(longitude) || isNaN(latitude)) {
    //         console.error("Invalid coordinates for station:", station);
    //         return { cx: 0, cy: 0 }; // You might want to handle this case differently
    //     }

    //     let point = new mapboxgl.LngLat(longitude, latitude);
    //     let { x, y } = map.project(point);
    //     return { cx: x, cy: y };
    // }

    // $: map?.on("move", (evt) => mapViewChanged++);

    // $: filteredMunicipalities = query
    //     ? municipalities.filter(
    //           (m) =>
    //               m.Name &&
    //               typeof m.Name === "string" &&
    //               m.Name.toLowerCase().includes(query.toLowerCase()),
    //       )
    //     : municipalities;

    // $: filteredStations = query
    //     ? stations.filter(
    //           (m) =>
    //               m.Community &&
    //               typeof m.Community === "string" &&
    //               m.Community.toLowerCase().includes(query.toLowerCase()) &&
    //               m.Name === "Coolidge Corner",
    //       )
    //     : stations;

    // function calculateBoundingBox(coordinates) {
    //     let bounds = new mapboxgl.LngLatBounds();

    //     coordinates.forEach((coord) => {
    //         bounds.extend(coord);
    //     });

    //     return bounds;
    // }

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

    <div style="display: flex; align-items: center; gap: 10px;">
        <div id="treeMap">
            {#if selectedComponent == 'zoning'}
                <!-- {console.log("HEREHEEE")}
                {console.log(transformedStopZoneDataForMunicipality)} -->
                <Treemap data={transformedStopZoneDataForMunicipality} />
            {:else if selectedComponent == 'usage'}
                <TreemapUsage data={transformedStopZoneUsageDataForMunicipality} />
            {/if}
        </div>

        <!-- <div id="treeMapUsage" class={treeMapUsageVisibility}>
            <h2>{treeMapUsageHeaderText}</h2>
            {#if transformedStopZoneUsageDataForMunicipality != undefined}
                <TreemapUsage data={transformedStopZoneUsageDataForMunicipality} />
            {:else}
                <p>Select A Municipality to View Usage Breakdown</p>
            {/if}
        </div> -->

        <div id="treeMapFuture">
            <h2>{treeMapFutureHeaderText}</h2>
            {#if transformedStopZoneDataForMunicipality != undefined}
                <TreemapFuture data={transformedStopZoneFutureDataForMunicipality} />
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
