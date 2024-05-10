<script>
    import mapboxgl from "mapbox-gl";
    import * as d3 from "d3";
    import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    import { onMount } from "svelte";
    import buffer from "@turf/buffer";
    import { point } from "@turf/helpers";
    import Treemap from "$lib/Treemap.svelte";
    import TreemapUsage from "$lib/TreemapUsage.svelte";
    import TreemapFuture from "$lib/TreemapFuture.svelte";

    let mapHeight = 0;
    let treeMapHeight = 0;
    let treeMapUsageHeight = 0;
    let treeMapFutureHeight = 0;
    let selectedComponent1 = 'zoning'; // Start with no component selected
    let selectedComponent2 = 'zoning';

    let updateKey = 0;
    mapboxgl.accessToken =
        "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";

    let map;
    let stations = [];
    let mapViewChanged = 0;
    let stationFlow = d3.scaleQuantize().domain([0, 1]).range([0, 0.5, 1]);
    let query = "";
    let municipalities = [];
    let municipalitiesFilter = -1;
    let input = "";
    let suggestions = [];
    let stopZoneData;
    let stopData;
    let brooklineStopZoneData;
    let coolidgeCornerStopZoneData;
    let transformedStopZoneDataForMunicipality1;
    let transformedStopZoneUsageDataForMunicipality;
    let transformedStopZoneFutureDataForMunicipality;

    let transformedStopZoneDataForMunicipality2;
    let transformedStopZoneUsageDataForMunicipality2;
    let transformedStopZoneFutureDataForMunicipality2;

    let parcelData;
    let treeMapHeaderText;
    let treeMapUsageHeaderText;
    let treeMapFutureHeaderText;
    let stopName = ''; 
    let stopName2 = ''; 

    function transformStopZoneData(originalData) {
            return [
                { name: "Single Family", value: originalData[0].properties.pctZonedAsSF, category1: "pctZonedAsSF" },
                { name: "Commerical", value: originalData[0].properties.pctUsedAsCommercial, category1: "pctZonedAsComm" },
                { name: "Multi Family", value: originalData[0].properties.pctZonedAsMultifamily, category1: "pctZonedAsMultifamily" },
            ];
    }

    function transformStopZoneUsageData(originalData) {
            return [
                { name: "Single Family", value: originalData[0].properties.pctUsedAsSF, category1: "pctUsedAsSF" },
                { name: "Commerical", value: originalData[0].properties.pctUsedAsCommerical, category1: "pctUsedAsCommerical" },
                { name: "Duplex", value: originalData[0].properties.pctUsedAsDuplex, category1: "pctUsedAsDuplex" },
                { name: "Triplex", value: originalData[0].properties.pctUsedAsTriplex, category1: "pctUsedAsTriplex" }
            ];
        }

    function transformStopZoneFutureData(originalData) {
            return [
                { name: "Single Family", value: originalData[0].properties.pctFutureZonedAsSF, category1: "pctFutureZonedAsSF" },
                { name: "Commercial", value: originalData[0].properties.pctZonedAsCommercial, category1: "isZonedAsCommercial" },
                { name: "Multi Family", value: originalData[0].properties.pctFutureZonedAsMulti, category1: "pctFutureZonedAsMulti" }
            ];
    }

    onMount(async () => {
        map = new mapboxgl.Map({
            container: "map",
            center: [-71.09451, 42.36027],
            zoom: 8,
            style: "mapbox://styles/smpeter/cluqd5hft05en01qqc4mxa1kd",
        });

        mapHeight = document.getElementById('map').clientHeight;
        treeMapHeight = document.getElementById('treeMap1').clientHeight;
        treeMapUsageHeight = document.getElementById('treeMapUsage1').clientHeight;

        //console.log("treeMapUsageHeight:", treeMapUsageHeight); 

        // Calculate the total height required
        const totalHeight = (mapHeight + treeMapHeight)*4;

        // Set the body height to accommodate both components
        document.body.style.height = `${totalHeight}px`;

        // Assuming 'map' is your Mapbox GL JS map instance
        // map.scrollZoom.disable();  // Disable scroll zoom
        // map.boxZoom.disable();     // Disable box zoom
        // map.dragPan.disable();     // Disable drag pan
        // map.dragRotate.disable();  // Disable drag rotate
        // map.keyboard.disable();    // Disable keyboard control
        // map.doubleClickZoom.disable(); // Disable double click zoom
        // map.touchZoomRotate.disable(); // Disable touch zoom and rotate
        await new Promise((resolve) => map.on("load", resolve));

        map.addSource("MBTALines", {
            type: "geojson",
            data: "/data/mbta_community_lines.geojson",
        });

        map.addLayer({
            id: "MAMBTALines",
            type: "line",
            source: "MBTALines",
            paint: {
                "line-color": ["get", "route_color"],
                "line-width": 2,
            },
        });


        municipalities = await d3.json("/data/mbta_municipalities.geojson");
        stations = await d3.json("/data/mbta_community_stops.geojson");

        stopZoneData = await d3.json(
            "/data/brookline_milton_stop_zone_census.geojson",
        );
        let brooklineStopZoneData = stopZoneData.features.filter(
            (feature) => feature.properties.community === "Brookline",
        );

        let coolidgeCornerStopZoneData = stopZoneData.features.filter(
            (feature) => feature.properties.stop_name === "Coolidge Corner",
        );

        let stopData = stopZoneData.features.filter(
            (feature) => feature.properties.stop_name === "Coolidge Corner",
        );
        
        // transformedStopZoneDataForMunicipality1 = transformStopZoneData(
        //    coolidgeCornerStopZoneData,
        //);

        //transformedStopZoneUsageDataForMunicipality = transformStopZoneUsageData(
        //    coolidgeCornerStopZoneData,
        //);

        //transformedStopZoneFutureDataForMunicipality = transformStopZoneFutureData(
        //    coolidgeCornerStopZoneData,
        //);

        parcelData = await d3.json(
            "/data/brookline_milton_parcels_dummies.geojson",
        );

        stations = stations.features.map((station) => {
            let newStation = {};
            newStation.Lat = station.geometry.coordinates[1];
            newStation.Long = station.geometry.coordinates[0];
            newStation.WithBuffer = buffer(
                point([newStation.Long, newStation.Lat]),
                0.5,
                { units: "miles" },
            ).geometry.coordinates[0];
            newStation.Community = station.properties.community;
            newStation.Name = station.properties.stop_name;
            newStation.Routes = station.properties.routes;
            newStation.RouteColors = station.properties.route_colors;
            newStation.Type = station.properties.mbta_comm_type;
            return newStation;
        });

        municipalities = municipalities.features.map((municipality) => {
            let newMunicipality = {};
            newMunicipality.PolygonCoordinates = [];

            if (
                municipality.geometry &&
                Array.isArray(municipality.geometry.coordinates[0])
            ) {
                newMunicipality.PolygonCoordinates =
                    municipality.geometry.coordinates[0];
            } else {
                console.log(municipality);
            }
            newMunicipality.Name = municipality.properties.community;
            newMunicipality.TotalHousingUnits =
                municipality.properties.housing_units_2020;
            newMunicipality.PopulationSize = municipality.properties.pop2020;
            newMunicipality.MBTACommunityType =
                municipality.properties.mbta_comm_type;
            newMunicipality.MinHousingCapacityRequirement =
                municipality.properties.min_rf1_cap_req;
            return newMunicipality;
        });
    });

    // Reactive statement to update suggestions based on input
    $: if (input) {
        console.log('input = ', input);
        suggestions = municipalities.filter(
            (m) =>
                m.Name &&
                typeof m.Name === "string" &&
                m.Name.toLowerCase().startsWith(input.toLowerCase()),
        );
        console.log('suggestions = ', suggestions);
    } else {
        suggestions = [];
    }
    

    $: treeMapVisibility = selectedComponent1 === 'zoning' ? 'visible' : 'hidden';
    $: treeMapUsageVisibility = selectedComponent1 === 'usage' ? 'visible' : 'hidden';

    $: treeMapVisibility2 = selectedComponent2 === 'zoning' ? 'visible' : 'hidden';
    $: treeMapUsageVisibility2 = selectedComponent2 === 'usage' ? 'visible' : 'hidden';

    $: if (stopName) {
        handleDropdownChange();
    }

    $: if (stopName2) {
        handleDropdownChange2();
    }

    function selectSuggestion(suggestion) {
        query = suggestion.Name; // Set the query to the selected municipality name
        suggestions = []; // Clear suggestions

        // Calculate the bounding box of the selected municipality
        const bounds = calculateBoundingBox(suggestion.PolygonCoordinates);

        treeMapHeaderText = `Zoning Breakdown for: ${suggestion.Name}`
        treeMapUsageHeaderText = `Usage Breakdown for: ${suggestion.Name}`

        // Update the map view to fit the bounding box with some padding
        map.fitBounds(bounds, { padding: 20 });
    }

    function handleDropdownChange() {
        console.log('Selected stopName = ', stopName);
        let stopData = stopZoneData.features.filter(
            (feature) => feature.properties.stop_name === stopName
        );
        
        // Check the data transformation here
        console.log("Filtered Stop Data", stopData);

        transformedStopZoneDataForMunicipality1 = transformStopZoneData(stopData);
        transformedStopZoneUsageDataForMunicipality = transformStopZoneUsageData(stopData);
        transformedStopZoneFutureDataForMunicipality = transformStopZoneFutureData(stopData);
    }

    function handleDropdownChange2() {
        console.log('Selected stopName2 = ', stopName2);
        let stopData2 = stopZoneData.features.filter(
            (feature) => feature.properties.stop_name === stopName2
        );
        
        // Check the data transformation here
        console.log("Filtered Stop Data 2 ", stopData2);

        transformedStopZoneDataForMunicipality2 = transformStopZoneData(stopData2);
        transformedStopZoneUsageDataForMunicipality2 = transformStopZoneUsageData(stopData2);
        transformedStopZoneFutureDataForMunicipality2 = transformStopZoneFutureData(stopData2);
    }

    function projectPolygonCoordinates(coordinates) {
        return coordinates
            .map((coord) => {
                let { cx, cy } = getCoords({ Lat: coord[1], Long: coord[0] });
                return `${cx},${cy}`;
            })
            .join(" ");
    }

    function getCoords(station) {
        const longitude = parseFloat(station.Long);
        const latitude = parseFloat(station.Lat);

        if (isNaN(longitude) || isNaN(latitude)) {
            console.error("Invalid coordinates for station:", station);
            return { cx: 0, cy: 0 }; // You might want to handle this case differently
        }

        let point = new mapboxgl.LngLat(longitude, latitude);
        let { x, y } = map.project(point);
        return { cx: x, cy: y };
    }

    $: map?.on("move", (evt) => mapViewChanged++);

    $: filteredMunicipalities = query
        ? municipalities.filter(
              (m) =>
                  m.Name &&
                  typeof m.Name === "string" &&
                  m.Name.toLowerCase().includes(query.toLowerCase()),
          )
        : municipalities;

    $: filteredStations = query
        ? stations.filter(
              (m) =>
                  m.Community &&
                  typeof m.Community === "string" &&
                  m.Community.toLowerCase().includes(query.toLowerCase()) &&
                  m.Name === "Coolidge Corner",
          )
        : stations;

    function calculateBoundingBox(coordinates) {
        let bounds = new mapboxgl.LngLatBounds();

        coordinates.forEach((coord) => {
            bounds.extend(coord);
        });

        return bounds;
    }

    
    
</script>
        <h1>Search</h1>
<div style="display: flex; align-items: center; gap: 10px;">
    <div>

        <input
            type="search"
            bind:value={input}
            aria-label="Municipality search"
            placeholder="🔍 Find your municipality"
        />
    </div>
    <br />


    <div>
        <select bind:value={stopName} on:change={handleDropdownChange}>
            <option value="">Select an option</option>
            <option value="Beaconsfield">Beaconsfield</option>
            <option value="Brandon Hall">Brandon Hall</option>
            <option value="Brookline Hills">Brookline Hills</option>
            <option value="Brookline Village">Brookline Village</option>
        </select>
    </div>

    <div>
        <select bind:value={stopName2} on:change={handleDropdownChange2}>
            <option value="">Select an option</option>
            <option value="Beaconsfield">Beaconsfield</option>
            <option value="Brandon Hall">Brandon Hall</option>
            <option value="Brookline Hills">Brookline Hills</option>
            <option value="Brookline Village">Brookline Village</option>
        </select>
    </div>
    
</div>

<br /> <br />

<div>
    {#if suggestions.length}
        <ul>
            {#each suggestions as suggestion}
                <li on:click={() => selectSuggestion(suggestion)}>
                    {suggestion.Name}
                </li>
            {/each}
        </ul>
    {/if}
</div>

{#key stopName}
  <div>
    <h3>{stopName}</h3>
    {#if stopName}
        <div style="display: flex; align-items: center; gap: 100px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <label style="cursor: pointer;">
                        <input type="radio" value="zoning" bind:group={selectedComponent1} />
                        Zoning
                    </label>
                    <label style="cursor: pointer;">
                        <input type="radio" value="usage" bind:group={selectedComponent1} />
                        Usage
                    </label>
                </div>
            
                <div id="treeMap1" class={treeMapVisibility}>
                    <h2>{treeMapHeaderText}</h2>
                    <Treemap id="treemap1" data={transformedStopZoneDataForMunicipality1} />
                </div>

                <div id="treeMapUsage1" class={treeMapUsageVisibility}>
                    <h2>{treeMapUsageHeaderText}</h2>
                    <TreemapUsage data={transformedStopZoneUsageDataForMunicipality} />
                </div>
                
            </div>

            <div id="treeMapFuture1">
                <h2>{treeMapFutureHeaderText}</h2>
                <TreemapFuture data={transformedStopZoneFutureDataForMunicipality} />
            </div>
        </div>
    {:else}
      <p></p>
    {/if}
  </div>
{/key}

{#key stopName2}
  <div>
    <h3>{stopName2}</h3>
    {#if stopName2}
        <div style="display: flex; align-items: center; gap: 100px;">
            <div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <label style="cursor: pointer;">
                        <input type="radio" value="zoning" bind:group={selectedComponent2} />
                        Zoning
                    </label>
                    <label style="cursor: pointer;">
                        <input type="radio" value="usage" bind:group={selectedComponent2} />
                        Usage
                    </label>
                </div>
            
                <div id="treeMap2" class={treeMapVisibility2}>
                    <h2>{transformedStopZoneDataForMunicipality2}</h2>
                    <Treemap id="treemap2" data={transformedStopZoneDataForMunicipality2} />
                </div>

                <div id="treeMapUsage2" class={treeMapUsageVisibility2}>
                    
                    <TreemapUsage data={transformedStopZoneUsageDataForMunicipality2} />
                </div>
                
            </div>

            <div id="treeMapFuture2">
                
                <TreemapFuture data={transformedStopZoneFutureDataForMunicipality2} />
            </div>
        </div>
    {:else}
      <p></p>
    {/if}
  </div>
{/key}




    <div>
        <div id="treeMap1" class={treeMapVisibility}>
            <h2></h2>
            {#if transformedStopZoneDataForMunicipality1 != undefined}
                
            {:else}
                
            {/if}
        </div>

        <div id="treeMapUsage1" class={treeMapUsageVisibility}>
            <h2></h2>
            {#if transformedStopZoneUsageDataForMunicipality != undefined}
                
            {:else}
              
            {/if}
        </div>
    </div>

    <div id="treeMapFuture1">
        
        {#if transformedStopZoneFutureDataForMunicipality != undefined}
           
        {:else}
        {/if}
    </div>

    


    <div>
        <div id="treeMap2" class={treeMapVisibility2}>
            <h2></h2>
            {#if transformedStopZoneDataForMunicipality2 != undefined}
                
            {:else}
                
            {/if}
        </div>

        <div id="treeMapUsage2" class={treeMapUsageVisibility2}>
            <h2></h2>
            {#if transformedStopZoneUsageDataForMunicipality2 != undefined}
                
            {:else}
              
            {/if}
        </div>
    </div>

    <div id="treeMapFuture2">
        
        {#if transformedStopZoneFutureDataForMunicipality2 != undefined}
           
        {:else}
        {/if}
    </div>




<br />
<div id="map">
    <svg>
        {#key mapViewChanged}
            {#each filteredMunicipalities as municipality, index}
                <polygon
                    id={`polygon-${index}`}
                    points={municipality.PolygonCoordinates.length
                        ? projectPolygonCoordinates(
                              municipality.PolygonCoordinates,
                          )
                        : ""}
                    fill="steelblue"
                    stroke="black"
                    stroke-width="1"
                    opacity="0.5"
                >
                    <title> {municipality.Name} </title>
                </polygon>
            {/each}
            {#each filteredStations as station}
                <polygon
                    data-station-name={station.Name}
                    points={projectPolygonCoordinates(station.WithBuffer)}
                    fill="#DD8155"
                    stroke="black"
                    stroke-width="1"
                    opacity="0.5"
                >
                    <title>
                        {station.Name}
                    </title>
                </polygon>
            {/each}
        {/key}
    </svg>
</div>



<br />

<style>
    @import url("$lib/global.css");

    :root {
        --color-departures: steelblue;
        --color-arrivals: darkorange;
    }

    #map {
        flex: 1;
    }

    #map svg {
        width: 100%;
        height: 100%;
        pointer-events: none;
        position: absolute;
        z-index: 1;

        circle {
            pointer-events: auto;
            fill-opacity: 60%;
            stroke: white;

            --color: color-mix(
                in oklch,
                var(--color-departures) calc(100% * var(--departure-ratio)),
                var(--color-arrivals)
            );
            fill: var(--color);
        }
    }

    .timescrubb {
        display: flex;
        gap: 1em;
        align-items: center;
        label {
            margin-left: auto;
        }
    }

    .legend > div {
        display: flex;
        align-items: center;
        gap: 0.5em;
        --color-departures: steelblue;
        --color-arrivals: darkorange;
        --color: color-mix(
            in oklch,
            var(--color-departures) calc(100% * var(--departure-ratio)),
            var(--color-arrivals)
        );
    }

    .legend {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 1em; /* Adjust based on your design */
        margin-block-start: 1rem;
        margin-block-end: 1rem;
        margin-block: 1em; /* Space above and below the legend */
        align-items: center;
    }

    .legend > div::before {
        content: "";
        display: inline-block;
        width: 20px; /* Swatch size */
        height: 20px; /* Swatch size */
        border-radius: 50%;
    }

    .legend > div:nth-child(1)::before {
        background-color: steelblue;
    }

    .legend > div:nth-child(2)::before {
        background-color: color-mix(
            in oklch,
            var(--color-departures) calc(100% * var(--departure-ratio)),
            var(--color-arrivals)
        );
    }

    .legend > div:nth-child(3)::before {
        background-color: darkorange;
    }

    .hidden {
        display: none;
    }
    
    .visible {
        display: block;
    }
    
</style>