<script>
    import mapboxgl from "mapbox-gl";
    import "../../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    import {onMount} from "svelte";

    mapboxgl.accessToken = "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";

    let map;
    let mapViewChanged = 0;
    export let bounds = [];
    export let stations = [];
    export let municipalities = [];

    onMount(async () => {
        map = new mapboxgl.Map({
            container: 'map',
            center: [-71.09451, 42.36027],
            zoom: 8,
            style: 'mapbox://styles/smpeter/cluqd5hft05en01qqc4mxa1kd',
        });
        // Assuming 'map' is your Mapbox GL JS map instance
        // map.scrollZoom.disable();  // Disable scroll zoom
        // map.boxZoom.disable();     // Disable box zoom
        // map.dragPan.disable();     // Disable drag pan
        // map.dragRotate.disable();  // Disable drag rotate
        // map.keyboard.disable();    // Disable keyboard control
        // map.doubleClickZoom.disable(); // Disable double click zoom
        // map.touchZoomRotate.disable(); // Disable touch zoom and rotate
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

    $: {
        if (bounds.length) {
            map?.fitBounds(bounds, { padding: 10 });
        }
    }

    export function fitBounds(bounds, padding) {
        map.fitBounds(bounds, { padding: 20 });
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

</script>

<div id="map">
    <svg>
        {#key mapViewChanged}
            {#each municipalities as municipality, index}
                <polygon
                        id={ `polygon-${index}` }
                        points={
                            municipality.PolygonCoordinates.length ?
                            projectPolygonCoordinates(municipality.PolygonCoordinates) : ""
                        }
                        fill="steelblue"
                        stroke="black"
                        stroke-width="1"
                        opacity="0.5"
                >
                    <title> { municipality.Name } </title>
                </polygon>
            {/each}
            {#each stations as station}
                <polygon
                        data-station-name={station.Name}
                        points= { projectPolygonCoordinates(station.WithBuffer) }
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
</style>
