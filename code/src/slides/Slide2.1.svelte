<script>
    import {onMount} from 'svelte';
    import Select from 'svelte-select';
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";
    import {observerStore} from '../lib/panelComponents/Scrolly_slide';

    export let active = false;
    export let municipality = null;
    export let station = null;

    export let value;
    let isVisible = false;

    const unsubscribe = observerStore.subscribe(store => {
        isVisible = store.isVisible;
    });

    // Reactive statement to monitor changes in value
    $: if (value === 5) {
        console.log(isVisible)
        observerStore.startObservation();
        console.log(isVisible)
    }


</script>

<div class="slide">
    {#if (municipality)}
        <h1>{municipality.Name}</h1>
        <p>
            {municipality.Name} is a {municipality.MBTACommunityType} community with a population
            of {municipality.PopulationSize} and
            {municipality.TotalHousingUnits} housing units. {municipality.Name} is currently compliant with the MBTA
            Communities Act as of April 2024, because they have submitted an acceptable action plan to the state. <br>
            <br>
        </p>
        {#if isVisible}
            {#if (municipality && !station)}
                <h2>SELECT a station in {municipality?.Name}</h2>
            {:else if (municipality && station)}
                <h2>Let's consider {station?.Name} in {municipality?.Name}</h2>
            {/if}
        {/if}

    {/if}

    <!-- <p>This is the first paragraph.</p>
    {#if isVisible}
      <p>This is the second paragraph that appears when the condition is met.</p>
    {/if} -->
</div>

<style>
    @import url("$lib/slide.css");

    .slide {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    p {
        margin: 0;
        padding: 1em;
        width: 100%;
        text-align: center;
    }
</style>
  