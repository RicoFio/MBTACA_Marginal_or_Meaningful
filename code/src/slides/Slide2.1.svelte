<script>
    import Select from 'svelte-select';
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";
    export let active = false;
    export let municipality = {};
    export let selectedStation = "";

</script>

<div class="slide">
    {#if (municipality)}
        <h1>{municipality.Name}</h1>
        <h3>
            {municipality.Name} is a {municipality.MBTACommunityType} community with a population of {municipality.PopulationSize} and 
            {municipality.TotalHousingUnits} housing units. {municipality.Name} is currently compliant with the MBTA Communities Act as of April 2024, because they have submitted an acceptable action plan to the state. <br> <br>

            Shapefiles for these MBTA communities come from the 2020 census, retrieved from Social Explorer. 

        </h3>
    {/if}
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
</style>