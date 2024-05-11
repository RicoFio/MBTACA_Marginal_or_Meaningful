<script>

    import Scrolly from "../panelComponents/Scrolly.svelte";
    import Slide1 from "../../slides/Slide1.svelte";
    import Slide11 from "../../slides/Slide1.1.svelte";
    import Slide2 from "../../slides/Slide2.svelte";
    import Slide21 from "../../slides/Slide2.1.svelte";
    import Slide3 from "../../slides/Slide3.svelte";
    import Slide4 from "../../slides/Slide4.svelte";
    import Slide5 from "../../slides/Slide5.svelte";
    import Slide6 from "../../slides/Slide6.svelte";
    import Slide7 from "../../slides/Slide7.svelte";

    let value;
    export let municipalities;
    export let stations;
    export let selectedMunicipality;
    export let selectedStations;
    export let guidedMode;
    export let comparisonMode;


    let colors = [
        '#05515e',
        '#629681',
        '#a9987a',
        '#9f9090',
        '#abafa7',
        '#dd8155',
        '#f39034',
        '#97340b',
        '#999624',
        '#3e5719',
    ];

    $: firstStation = selectedStations[0];
</script>

<div class="panel" style="position: absolute; top: 0; left: 0; width: 40%; height: 100%; background-color: rgba(0, 0, 0, 0.6); padding: 20px; color: {colors[3]};">
    <Scrolly bind:value>
        <Slide1 active={value === 0} />
        <Slide11 active={value === 1} />
        <Slide2 active={value === 2}  bind:municipalities={municipalities} bind:selectedMunicipality={selectedMunicipality}/>
        <Slide21 active={value === 3} bind:municipality={selectedMunicipality}/>
        <Slide3 active={value === 4}  bind:municipality={selectedMunicipality} bind:station={firstStation}/>
        <Slide4 active={value === 5}  bind:municipality={selectedMunicipality} bind:station={firstStation}/>
        <Slide5 active={value === 6}  bind:municipality={selectedMunicipality} bind:station={firstStation}/>
        <Slide6 active={value === 7}  bind:municipality={selectedMunicipality} bind:stations={selectedStations} bind:comparisonMode={comparisonMode}/>
        <Slide7 active={value === 8} />
    </Scrolly>
</div>

<style>
    div {
        z-index: 5;
        text-align: center;
    }

    .panel {
        overflow-y: auto;  /* Allows vertical scrolling */
        overflow-x: hidden; /* Disables horizontal scrolling */
    }

    .panel::-webkit-scrollbar {
        display: none;
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

    /* .step {
		height: 80vh;
		opacity: .3;
		background: plum;
		transition: opacity 300ms ease;
		display: flex;
		justify-content: center;
		place-items: center;
	}
	
	.step.active {
		opacity: 1;
	} */

</style>

  