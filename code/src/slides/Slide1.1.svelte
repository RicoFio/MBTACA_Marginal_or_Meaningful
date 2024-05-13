<script>
    export let active = false;
    import { observerStore } from '../lib/panelComponents/Scrolly_slide';

    export let value;
    let isVisible = false;

    const unsubscribe = observerStore.subscribe(store => {
        isVisible = store.isVisible;
    });
    
    // Reactive statement to monitor changes in value
    $: if (value === 1) {
        console.log(isVisible)
        observerStore.startObservation();
        console.log(isVisible)
    }
</script>

<div class="slide">
    <h1>What is the MBTA Communities Act?</h1>
    {#if isVisible}
    <h2>
      The MBTA Communities Act is a 2021 Massachusetts state law that aims to reduce the housing crisis by requiring cities near MBTA stations to upzone at least one area within their borders, allowing multi-family housing without an extensive permitting process. Massachusetts governor Maura Healy has stated that noncompliance could result in result in not only a loss of state funding for housing but also potential legal action. <br>
        </h2>
        <br>
        <div class="scroll-indicator"></div>
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

    .slide .scroll-indicator {
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 15px solid white; /* Adjust color to match your slide's theme */
    margin: 20px auto; /* Centers the arrow and adds space above it */
    animation: bounce 2s infinite; /* Adds a bouncing animation to catch attention */
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-20px);
    }
    60% {
        transform: translateY(-10px);
    }
}
</style>