<script>
    import mapboxgl from "mapbox-gl";
    import "../../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    import { onMount } from "svelte";
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";

    mapboxgl.accessToken = "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";

    let map;
    let mapViewChanged = 0;
    export let bounds = [];
    export let stations = [];
    export let municipalities = [];
    export let selectedStations = [];
    export let selectedMunicipality = null;
    export let guidedMode = true;
    export let parcelFiles = [];

    onMount(async () => {
        map = new mapboxgl.Map({
            container: 'map',
            center: [-71.09451-1.2, 42.36027],
            zoom: 8,
            style: 'mapbox://styles/smpeter/cluqd5hft05en01qqc4mxa1kd',
            attributionControl: false,
        });
        // Assuming 'map' is your Mapbox GL JS map instance
        map.scrollZoom.disable();  // Disable scroll zoom
        map.boxZoom.disable();     // Disable box zoom
        map.dragPan.disable();     // Disable drag pan
        map.dragRotate.disable();  // Disable drag rotate
        map.keyboard.disable();    // Disable keyboard control
        map.doubleClickZoom.disable(); // Disable double click zoom
        map.touchZoomRotate.disable(); // Disable touch zoom and rotate
        await new Promise(resolve => map.on("load", resolve));

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
    })

    $: map?.on("move", evt => mapViewChanged++);

    // /**
    //  * Fits the map bounds with specified padding.
    //  * @param {Object} bounds - The bounds to fit the map to.
    //  * @param {(number|Object)} padding - The padding as a number or an object with optional top, bottom, left, and right properties.
    //  */
    export function fitBounds(bounds, padding = { padding: 20 }) {
        map.fitBounds(bounds, padding);
    }

    function projectPolygonCoordinates(coordinates) {
        return coordinates.map(coord => {
            let { cx, cy } = getCoords({ Lat: coord[1], Long: coord[0] });
            return `${cx},${cy}`;
        }).join(' ');
    }

    function getCoords(station) {

        const longitude = parseFloat(station.Long);
        const latitude = parseFloat(station.Lat);

        if (isNaN(longitude) || isNaN(latitude)) {
            console.error("Invalid coordinates for station:", station);
            return { cx: 0, cy: 0 }; // You might want to handle this case differently
        }

        let point = new mapboxgl.LngLat(longitude, latitude);
        let {x, y} = map.project(point);
        return {cx: x, cy: y};
    }

    function toggleStation(station) {
        if (!selectedStations.some(s => s.Name === station.Name)) {
            if ((guidedMode && selectedStations.length < 1) || (!guidedMode && selectedStations.length < 2)) {
                selectedStations = [...selectedStations, station];
            } else {
                console.log("Toggle station not possible");
            }
        } else if (guidedMode) {

        }
        else {
            selectedStations = selectedStations.filter(s => s.Name !== station.Name);
        }
    }

    $: {

    }

    $: {
        if (guidedMode && selectedStations.length > 0) {
            const station = selectedStations[0];
            let bounds = calculateBoundingBox({type:'Polygon', coordinates: [station.getBuffer(0.5)]});

            fitBounds(bounds, {
                padding: {top: 20, bottom: 20, left: 1000, right: 20}
            });
        }
    }

    $: filteredMunicipalities = selectedMunicipality ? municipalities.filter(m => {
        return m.Name == selectedMunicipality.Name
    }) : municipalities;

    $: filteredStations = selectedMunicipality ? stations.filter(s => {
        return s.Community == selectedMunicipality.Name
    }) : stations;

</script>

<div id="map">
    <svg>
        {#key mapViewChanged}
            {#each filteredMunicipalities as municipality, index}
                {#if municipality.Geometries.type === "Polygon"}
                    <polygon
                            id={ `polygon-${index}` }
                            points={
                                municipality.Geometries.coordinates.length ?
                                projectPolygonCoordinates(municipality.Geometries.coordinates[0]) : ""
                            }
                            fill="steelblue"
                            stroke="black"
                            stroke-width="1"
                            opacity="0.5"
                    >
                        <title> { municipality.Name } </title>
                    </polygon>
                {:else if municipality.Geometries.type === 'MultiPolygon'}
                    {#each municipality.Geometries.coordinates as geometry}
                        <polygon
                                id={ `polygon-${index}` }
                                points={
                                municipality.Geometries.coordinates.length ?
                                projectPolygonCoordinates(geometry[0]) : ""
                            }
                                fill="steelblue"
                                stroke="black"
                                stroke-width="1"
                                opacity="0.5"
                        >
                            <title> { municipality.Name } </title>
                        </polygon>
                    {/each}
                {/if}
            {/each}
            {#each filteredStations as station, index (station.Name)}
                <polygon
                        class:station
                        class:selected={selectedStations.some(s => s.Name === station.Name)}
                        data-station-name={station.Name}
                        points={projectPolygonCoordinates(station.getBuffer(
                            selectedStations.some(s => s.Name === station.Name) ?
                            0.5 :
                            0.1
                        ))}
                        fill={selectedStations.some(s => s.Name === station.Name) ? 'red' : '#DD8155'}
                        stroke="black"
                        stroke-width="1"
                        opacity={selectedStations.some(s => s.Name === station.Name) ? '0.8' : '0.5'}
                        role="button"
                        tabindex="0"
                        aria-label={`Select station ${station.Name}`}
                        on:click={() => toggleStation(station)}
                        on:keyup={event => event.key === 'Enter' && toggleStation(station)}
                >
                    <title>{station.Name}</title>
                </polygon>
            {/each}
        {/key}
    </svg>
</div>

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
        cursor: grab;

        .station {
            pointer-events: auto;
            cursor: pointer;
            fill-opacity: 60%;
            stroke: white;

            --color: color-mix(
                    in oklch,
                    var(--color-departures) calc(100% * var(--departure-ratio)),
                    var(--color-arrivals)
            );
            fill: var(--color);
        }
        .station.selected {
            /* Styles for selected stations */
            fill: red;
            opacity: 0.8;
        }
    }
</style>
