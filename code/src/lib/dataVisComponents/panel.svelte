<script>

    import Scrolly from "../panelComponents/Scrolly.svelte";
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
    <h1>MARGINAL OR MEANINGFUL?</h1>
    <h2>An immersive tool for exploring the impacts of the MBTA Communities Act</h2>
    <p>- Amelia Baum, Riccardo Fiorista, Simone Peter, Ravi Tejwani -</p>
    <Scrolly bind:value> <!-- 3. This is what updates value -->
        {#each ['MARGINAL', 'OR', 'World!'] as text, i}
            <div class="step" class:active={value === i}> <!-- 4. Dynamically applies the active class -->
                <p>{text}</p> 
            </div>
        {/each}
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

  