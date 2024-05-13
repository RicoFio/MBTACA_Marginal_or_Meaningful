<script>
    export let active = false;
    import {observerStore} from '../lib/panelComponents/Scrolly_slide';

    export let value;
    let isVisible = false;
    let isVisibleSecond = false;

    observerStore.subscribe(store => {
        isVisible = store.isVisible;
    });

    $: if (value === 2) {
        observerStore.resetVisibility();  // Reset visibility whenever checking this condition
        observerStore.startObservation();
    }

    $: if (isVisible) {
        setTimeout(() => {
            isVisibleSecond = true;
        }, 8000);
    }
</script>


<div class="slide">
    <h1>What are the controversies?</h1>
    {#if isVisible}
        <p>
            While broadly supported, the law faces controversy, especially in lower-density suburbs served by MBTA
            Commuter Rail. As of April 2024, all 177 communities have submitted appropriate zoning proposals to the
            state and thus are technically compliant with the law, but many, including Holden, Rockford, and Bourne,
            raised significant legal challenges along the way, and whether all communities will become compliant remains
            to be seen. On the other hand, some communities, such as Brookline, have embraced the legislation and have
            passed new zoning regulations that go above and beyond the law’s requirements. <br>
        </p>
    {/if}
    <br>
    {#if isVisibleSecond}
        <p>
            Though critics have claimed that upzoning these suburban communities would significantly change the urban
            form of low-density communities in culturally incompatible ways, it is essential to understand that the MBTA
            Communities Act does not directly dictate what type of housing is built in these communities. It simply
            requires a single district within the municipality where some form of multifamily housing is allowed by
            right. This gives local governments significant influence on the location and nature of their multifamily
            districts. <br>
        </p>
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