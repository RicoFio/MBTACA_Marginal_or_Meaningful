<script>
    import Select from 'svelte-select';
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";
    export let active = false;
    export let selectedMunicipality = "";
    export let selectedStation = "";

</script>

<div class="slide">
    {#if (selectedMunicipality && !selectedStation)}
        <h1>Select a station in {selectedMunicipality.Name}</h1>
    {:else}
        <h1>Let's consider {selectedStation?.Name} in {selectedMunicipality.Name}</h1>
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