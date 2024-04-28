<script>

    import Scrolly from "../panelComponents/Scrolly.svelte";
    import Slide1 from "../../slides/Slide1.svelte"
    import Slide2 from "../../slides/Slide2.svelte"
    import Slide3 from "../../slides/Slide3.svelte"
    let value;
    // $: console.log({ value });
    let colors = [
        '#05515e',
        '#629681',
        '#a9987a',
        '#9f9090',
        '#abafa7',
        '#dd8155',
        '#dd8155',
        '#dd8155',
        '#999624',
        '#3e5719',
    ];
</script>

<div class="panel" style="position: absolute; top: 0; left: 0; width: 40%; height: 100%; background-color: rgba(0, 0, 0, 0.6); padding: 20px; color: {colors[3]};">
    <Scrolly bind:value> <!-- 3. This is what updates value -->
        <!-- {#each ['MARGINAL', 'OR', 'World!'] as text, i}
            <div class="step" class:active={value === i}>
                <p>{text}</p> 
            </div>
        {/each} -->
        <Slide1 active={value === 0} />
        <Slide2 active={value === 1} />
        <Slide3 active={value === 2} />
    </Scrolly>
</div>

<style>
    div {
        z-index: 5;
        text-align: center;
    }

    .panel {
        overflow: scroll;
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

    .step {
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
	}

</style>

  