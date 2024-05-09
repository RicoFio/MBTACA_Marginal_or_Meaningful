<script>
     import { onMount } from 'svelte';
    import Select from 'svelte-select';
    import { calculateBoundingBox } from "$lib/mapComponents/mapUtils.js";
    export let active = false;
    export let municipality = null;
    export let station = null;
  
    export let value = 0;
    let isVisible = false;
    let observer;
    let timeout;
  
    $: console.log(value)
    // Reactive statement to monitor changes in value
    $: if (value === 4) {
        console.log("EHRHERHE")
      startObservation();
    }
  
    function startObservation() {
      if (observer) {
        observer.disconnect(); // Disconnect existing observer if any
      }

      const rootElement = document.querySelector('.slide');

      observer = new IntersectionObserver(handleIntersect, {
        root: rootElement,
        threshold: 0.5, // Adjust threshold as needed
        rootMargin: '0px'
      });
  
      const firstParagraph = document.querySelector('.slide > p:first-of-type');
      if (firstParagraph) {
        observer.observe(firstParagraph);
      }
    }
  
    function handleIntersect(entries) {
      const [entry] = entries;
      clearTimeout(timeout);

      if (entry.isIntersecting) {
        // Set the isVisible to true after a delay of 5 seconds
        timeout = setTimeout(() => {
          isVisible = true;
        }, 3000);  // 5000 milliseconds = 5 seconds
      } else {
        isVisible = false;
      }
      console.log("Intersection observed:", isVisible);
      console.log("Bounding client rect:", entry.boundingClientRect);
      console.log("Intersection ratio:", entry.intersectionRatio);
      console.log("Intersection rect:", entry.intersectionRect);
}
  
    onMount(() => {
      // Disconnect the observer when the component is destroyed
      return () => {
        if (observer) {
          observer.disconnect();
        }
      };
    });
  </script>
  
  <div class="slide">
    {#if (municipality)}
        <h1>{municipality.Name}</h1>
        <h3>
            {municipality.Name} is a {municipality.MBTACommunityType} community with a population of {municipality.PopulationSize} and 
            {municipality.TotalHousingUnits} housing units. {municipality.Name} is currently compliant with the MBTA Communities Act as of April 2024, because they have submitted an acceptable action plan to the state. <br> <br>

            Shapefiles for these MBTA communities come from the 2020 census, retrieved from Social Explorer. <br> <br>
        </h3>
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
  