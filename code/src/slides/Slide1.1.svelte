<script>
    export let active = false;
    export let absolute_slide_value = 1;
    import { observerStore } from '../lib/panelComponents/Scrolly_slide';

    let entered = 0;
    $: if (active && entered == 0) {
        absolute_slide_value = 1;
        entered += 1;
    }

    export let value = 0;
    export let isVisible_slide1 = false;
    export let visibility_slide12 = false;

    const unsubscribe = observerStore.subscribe(store => {
        isVisible_slide1 = store.isVisible;
    });

    // $: if (isVisible_slide1) {
    //   console.log(visibility_slide12)
    //   visibility_slide12 = 'value === 2';
    //   value = 2;
    //   console.log("Slide12 is now")
    //   console.log(visibility_slide12)
    // }
    
    // Reactive statement to monitor changes in value
    $: if (value === 1) {
        observerStore.startObservation();
    }
</script>

<div class="slide">
  {console.log("abs", absolute_slide_value)}
    <h1>What is the MBTA Communities Act?</h1>
    {#if isVisible_slide1}
    <h2>
      The MBTA Communities Act is a 2021 Massachusetts state law that aims to reduce the housing crisis by requiring cities near MBTA stations to upzone at least one area within their borders, allowing multi-family housing without an extensive permitting process. Massachusetts governor Maura Healy has stated that noncompliance could result in result in not only a loss of state funding for housing but also potential legal action. <br>
        </h2>
      {/if}
</div>

<!-- <div class="footnotes">
    <ol>
      <li id="fn1">
        https://www.wbur.org/radioboston/2023/11/27/mbta-communites-act-density-transit-oriented-housing
        <a href="#fnref1">↩</a>
      </li>
    </ol>
  </div> -->

<style>
    @import url("$lib/slide.css");
    .footnotes {
      font-size: smaller;
      border-top: 1px solid #ccc;
      padding-top: 5px;
    }

    .footnotes ol {
      padding-left: 0;
    }

    .footnotes li {
      list-style: none; /* Removes default list styling */
    }

    .footnotes sup a {
      text-decoration: none;
    }
</style>