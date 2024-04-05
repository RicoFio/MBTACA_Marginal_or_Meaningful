<script>
    import mapbox from 'mapbox-gl';
    const MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";
    export let geoJsonToFit;
    console.log(MAPBOX_ACCESS_TOKEN, 'is not defined. Check your .env.local file.');
    mapbox.accessToken = MAPBOX_ACCESS_TOKEN;

    let container;
    let map;

    function load() {
        map = new mapbox.Map({
            container,
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [-71.057083, 42.361145],
            zoom: 8,
            maxBounds: [[-179,-60],[179,80]]
        });

        map.on("load", () => {
            map.addControl(new mapbox.NavigationControl({
                showCompass: false
            }))
            updateBounds()
            map.on("zoom", updateBounds);
            map.on("drag", updateBounds);
            map.on("move", updateBounds);
        });
    }

    function updateBounds() {
        const bounds = map.getBounds()
        geoJsonToFit.features[0].geometry.coordinates = [bounds._ne.lng, bounds._ne.lat]
        geoJsonToFit.features[1].geometry.coordinates = [bounds._sw.lng, bounds._sw.lat]
    }

</script>

<svelte:head>
    <link
            rel="stylesheet"
            href="https://unpkg.com/mapbox-gl/dist/mapbox-gl.css"
            on:load={load}
    />
</svelte:head>

<div bind:this={container}>
</div>

<style>
    div {
        width: 100%;
        height: 100%;
    }
</style>