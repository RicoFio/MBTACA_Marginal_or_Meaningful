<script>
    import Select from 'svelte-select';

    export let active = false;
    export let municipalities = [];
    export let selectedMunicipality = {};
    let input = "";

    function handleSelect(e) {
        selectedMunicipality = e.detail.value;
    }

    $: items = municipalities?.map(m => ({
        'value': m,
        'label': m.Name
        // 'selectable': m.Selectable
    }));

    const searchable = true;
</script>

{#if (active)}
    <div class="slide">
        <p>
            Use this interactive map to explore the potential effects of siting multifamily districts near different
            transit stations within communities. In addition to providing detailed parcel-level information about
            current zoning and usage patterns and how these might change if upzoning were to occur, the tool provides
            relevant demographic statistics about the area surrounding each MBTA station.
        </p>
        <br>
        <br>
        <br>
        <br>
        <div class="select-container">
            <Select {items} {searchable} on:change={handleSelect} on:click={handleSelect} class="searchbar"
                    placeholder="Please select a municipality"/>
        </div>
    </div>
{/if}

<style>
    @import url("$lib/global.css");
    @import url("$lib/slide.css");

    :global(.searchbar) {
        z-index: 100;
        font: 18px sans-serif;
        font-family: 'Montserrat', sans-serif;
        visibility: visible;
        background-color: rgba(10, 0, 0, 0.4) !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 10px;
        width: 200px;
        color: #a9987a;
        position: fixed;
        padding: 10px;
    }

    .select-container {
        width: 40%;
    }
</style>