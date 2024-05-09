<script>
    import Select from 'svelte-select';
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";
    export let active = false;
    export let municipality = null;
    export let station = null;
</script>

<div class="slide">
    {#if (municipality && !station)}
        <h1>Select a station in {municipality?.Name}</h1>
    {:else if (municipality && station)}
        <h1>Let's consider {station?.Name} in {municipality?.Name}</h1>
    {/if}
</div>

<style>
    @import url("$lib/slide.css");
</style>