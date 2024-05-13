<script>
    export let active = false;
    import {observerStore} from '../lib/panelComponents/Scrolly_slide';

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
        <p>
            The MBTA Communities Act is a 2021 Massachusetts state law that aims to reduce the housing crisis by
            requiring cities near MBTA stations to upzone at least one area within their borders, allowing multi-family
            housing without an extensive permitting process. Massachusetts governor Maura Healy has stated that
            noncompliance could result in result in not only a loss of state funding for housing but also potential
            legal action. <br>
        </p>
        <br>
        <div class="scroll-indicator"></div>
    {/if}
</div>

<style>
    @import url("$lib/slide.css");
    @import url("$lib/arrow.css");

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