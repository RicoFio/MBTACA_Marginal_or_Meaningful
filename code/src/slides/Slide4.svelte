<script>
    export let active = false;
    import ForceGraph from "../lib/dataVisComponents/ForceGraph.svelte";
    import ForceGraphSelector from "../lib/dataVisComponents/ForceGraphSelector.svelte"

    const data = {
                    "age": [
                        {label: 'age group 1', value: 20},
                        {label: 'age group 2', value: 80},
                        {label: 'age group 3', value: 40},
                    ],
                    "race": [
                        {label: 'race group 1', value: 30},
                        {label: 'race group 2', value: 60},
                        {label: 'race group 3', value: 50},
                    ],
                    "gender": [
                        {label: 'male', value: 50},
                        {label: 'female', value: 90},
                    ],
                    "income": [
                        {label: 'income group 1', value: 80},
                        {label: 'income group 2', value: 20},
                        {label: 'income group 3', value: 40},
                        {label: 'income group 4', value: 50},
                    ],
                    "cars per household": [
                        {label: 'none', value: 20},
                        {label: 'one', value: 50},
                        {label: 'two or more', value: 90},
                    ],
                    "mode of transportation": [
                        {label: 'car', value: 90},
                        {label: 'train', value: 60},
                        {label: 'bike', value: 20},
                        {label: 'walk', value: 10},
                        {label: 'other', value: 10}
                    ]
                }
    let activeSelection = "age"
    $: current_data = data[activeSelection]
</script>

<div class="slide">
    <h1>MUNICIPALITY: Station Name</h1>
    <h2>Some explanations etc</h2>
    <p>explanations blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <h2>WHO LIVES HERE? - let's find out</h2>
    <ForceGraphSelector bind:activeSelection></ForceGraphSelector>

    {#key current_data} <!--forcing visualization to re-render when data is updated -->
    <ForceGraph
                cssHeight=50
                cssWidth=40
                data={ current_data }
                selectedCategory = { activeSelection }
            />
    {/key}
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