<script>
    import {projectPolygonCoordinates} from "$lib/mapComponents/mapUtils.js";
    export let municipalities;
    export let projectOnMap;
</script>

<svg>
    {#each municipalities as municipality, index}
        <polygon
                id={ `polygon-${index}` }
                points={
                                municipality.PolygonCoordinates.length ?
                                projectPolygonCoordinates(municipality.PolygonCoordinates, projectOnMap) : ""
                            }
                fill="steelblue"
                stroke="black"
                stroke-width="1"
                opacity="0.5"
        >
            <title> { municipality.Name } </title>
        </polygon>
    {/each}
</svg>
