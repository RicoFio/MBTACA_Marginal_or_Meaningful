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
    }));

    const searchable = true;
</script>


<div class="slide">
    <Select {items} {searchable} on:change={handleSelect} on:click={handleSelect}/>
</div>

<style>
    @import url("$lib/global.css");
    .slide {
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        pointer-events: auto;
        z-index: 0;
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