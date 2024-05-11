<script>
     import { onMount } from 'svelte';
    import Select from 'svelte-select';
    import { calculateBoundingBox } from "$lib/mapComponents/mapUtils.js";
    import { observerStore } from '../lib/panelComponents/Scrolly_slide';

    export let active = false;
    export let municipality = null;
    export let station = null;
  
    export let value = 0;
    let isVisible_slide21 = false;

    const unsubscribe = observerStore.subscribe(store => {
        isVisible_slide21 = store.isVisible;
    });
    
    // Reactive statement to monitor changes in value
    $: if (value === 5) {
        observerStore.startObservation();
    }

  
    
  </script>
  
  {#if (active)}
  <div class="slide">
    {#if (municipality)}
        <h1>{municipality.Name}</h1>
        <h3>
            {municipality.Name} is a {municipality.MBTACommunityType} community with a population of {municipality.PopulationSize} and 
            {municipality.TotalHousingUnits} housing units. {municipality.Name} is currently compliant with the MBTA Communities Act as of April 2024, because they have submitted an acceptable action plan to the state. <br> <br>

            Shapefiles for these MBTA communities come from the 2020 census, retrieved from Social Explorer. <br> <br>
        </h3>
        {#if isVisible_slide21}
        {#if (municipality && !station)}
                <h2>SELECT a station in {municipality?.Name}</h2>
            {:else if (municipality && station)}
                <h2>Let's consider {station?.Name} in {municipality?.Name}</h2>
            {/if}
        {/if}

    {/if}
  </div>
  {/if}
  
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
  