<script>
    import Select from 'svelte-select';
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";

    export let active = false;
    export let municipality;
    export let stations;
    export let comparisonMode;


    $: firstStation = (stations?.length > 0) ? stations[0] : undefined;
    $: secondStation = (stations?.length > 1) ? stations[1] : undefined;

    $: {
        console.log("stations");
        console.log(stations);
        console.log("firstStation");
        console.log(firstStation);
        console.log("secondStation");
        console.log(secondStation);
    }

    $: {
        if (active) {
            comparisonMode = true;
        }
    }

</script>

<div class="slide">
    {#if (municipality && !firstStation)}
        <h1>Select a station in {municipality?.Name}</h1>
    {:else if (municipality && firstStation && !secondStation)}
        <h1>Select a second station in {municipality?.Name}</h1>
    {:else}
        <h1>Let's consider {firstStation?.Name} and {secondStation?.Name} in {municipality?.Name}</h1>
    {/if}
</div>

<style>
    @import url("$lib/slide.css");
</style>
