<script>
    import Select from 'svelte-select';
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";
    export let active = false;
    export let municipality = {};
    export let station = {};
</script>

<div class="slide">
    {#if (JSON.stringify(municipality) !== '{}' && JSON.stringify(station) === '{}')}
        <h1>Select a station in {municipality?.Name}</h1>
    {:else if (JSON.stringify(municipality) !== '{}' && JSON.stringify(station) !== '{}')}
        <h1>Let's consider {station?.Name} in {municipality?.Name}</h1>
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