<script>
    import { geoMercator } from "d3";
    import MapboxMap from '$lib/map/MapboxMap.svelte';
    import SvgMap from '$lib/map/SvgMap.svelte';

    // This geoJSON is used to sync the Mapbox map and the SVG map
    let geoJsonToFit = {
        type: "FeatureCollection",
        features: [
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [1, 0],
                },
            },
            {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [0, 1],
                },
            },
        ],
    };

    let width;
    let height;

    $: projection = geoMercator().fitSize([width, height], geoJsonToFit);

    let activeLayer = 'concentric';
</script>
<div class="maps-container" bind:clientWidth={width} bind:clientHeight={height}>
    <MapboxMap bind:geoJsonToFit>
    </MapboxMap>
    <div class="svg-map-container">
        <SvgMap {width} {height} {projection} {activeLayer}></SvgMap>
    </div>
</div>

<style>
    .maps-container {
        width: 100%;
        height: 100vh;
        position: relative;
    }
    .svg-map-container {
        position: absolute;
        top: 0;
        left: 0;
        pointer-events: none;
    }
</style>
