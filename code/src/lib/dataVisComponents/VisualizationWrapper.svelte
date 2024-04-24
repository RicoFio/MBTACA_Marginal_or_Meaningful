<script>
    import { onMount } from "svelte";

    export let div;
    export let cssHeight;
    export let cssWidth;
    export let loaded = true;
    export let mousemove;
    export let mouseleave;
    export let id;

    // export let onmount;
    export let chartWidth = 0;
    export let chartHeight = 0;


    function resize() {
        chartWidth = div.clientWidth;
        chartHeight = div.clientHeight;
    }

    onMount(() => {
        resize();
        loaded = true;
    })
</script>

<svelte:window on:resize='{resize}'/>

<div 
    bind:this={div}
    style={`
        height: ${cssHeight}vh;
        width: ${cssWidth}vw;
    `}
    class='viz'
>
    {#if loaded}
        <svg 
            width={chartWidth}
            height={chartHeight}
            on:mousemove={mousemove}
            on:mouseleave={mouseleave}
            id={id}
        >
            <slot />
        </svg>
    {:else}
        <div class="loading">Loading...</div>
    {/if}
</div>

<style>
    .viz {
        /* background-color: red; */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>