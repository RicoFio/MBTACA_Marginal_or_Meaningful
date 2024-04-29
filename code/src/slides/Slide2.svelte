<script>
    import Select from 'svelte-select';
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";
    export let active = false;
    export let municipalities = [];
    export let selectedMunicipality = "";
    let input = "";

    let suggestions = [];

    // Reactive statement to update suggestions based on input
    $: if (input) {
        suggestions = municipalities.filter(m =>
            m.Name && typeof m.Name === 'string' && m.Name.toLowerCase().startsWith(input.toLowerCase())
        );
    } else {
        suggestions = [];
    }

    function selectSuggestion(suggestion) {
        selectedMunicipality = suggestion.Name;
        suggestions = [];
        input = "";
    }

</script>

<div class="slide">
    <div>
        <h1>Search</h1>
        <input type="search" bind:value={input}
               aria-label="Municipality search" placeholder="🔍 Find your municipality" />
        {#if suggestions.length}
            {#each suggestions as suggestion}
                <h2 on:click={() => selectSuggestion(suggestion)}>
                    {suggestion.Name}
                </h2>
            {/each}
        {/if}
    </div>
</div>

<style>
    .slide {
        height: 100vh; 
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    h1 {
        font-weight: normal;
    }

    h2 {
        font-weight: normal;
    }

    h3 {
        font-weight: normal;
    }
</style>