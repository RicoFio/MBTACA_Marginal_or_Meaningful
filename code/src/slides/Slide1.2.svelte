<script>
    export let active = false;
    import { observerStore } from '../lib/panelComponents/Scrolly_slide';

    export let value = 0;
    let isVisible_slide12 = false;
    let isVisibleSecond_slide12 = false;
    export let isSlide2Active;

    observerStore.subscribe(store => {
        isVisible_slide12 = store.isVisible;
    });

    $: if (value === 2) {
        // observerStore.resetVisibility();  // Reset visibility whenever checking this condition
        console.log("observation started")
        observerStore.startObservation();
    }

    $: if (isVisible_slide12) {
        console.log("entered", isVisible_slide12)
            setTimeout(() => {
                isVisibleSecond_slide12 = true;
            }, 15000);
            console.log("is visible second slide12 now true")
        }
    $: if (isVisibleSecond_slide12 == true) {
        console.log("is visible", isVisibleSecond_slide12)
        isSlide2Active = 'value === 3';
        console.log("slide 2 is now active", isSlide2Active)
    }
</script>

{#if (active)}
<div class="slide">
    <h1>What are the controversies?</h1>
    {#if isVisible_slide12}
        <h2>
      While broadly supported, the law faces controversy, especially in lower-density suburbs served by MBTA Commuter Rail. As of April 2024, all 177 communities have submitted appropriate zoning proposals to the state and thus are technically compliant with the law, but many, including Holden, Rockford, and Bourne, raised significant legal challenges along the way, and whether all communities will become compliant remains to be seen. On the other hand, some communities, such as Brookline, have embraced the legislation and have passed new zoning regulations that go above and beyond the law’s requirements. <br>
    </h2>
      {/if}
      <br>
      {#if isVisibleSecond_slide12}
    <h2>
      Though critics have claimed that upzoning these suburban communities would significantly change the urban form of low-density communities in culturally incompatible ways, it is essential to understand that the MBTA Communities Act does not directly dictate what type of housing is built in these communities. It simply requires a single district within the municipality where some form of multifamily housing is allowed by right. This gives local governments significant influence on the location and nature of their multifamily districts. <br>
        </h2>
    {/if}
</div>
{/if}

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