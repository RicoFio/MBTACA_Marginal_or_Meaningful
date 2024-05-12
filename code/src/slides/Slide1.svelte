<script>
    import MultiPieChart from "$lib/dataVisComponents/MultiPieChart.svelte";
    import MultiPieChartWithText from "$lib/dataVisComponents/MultiPieChartWithText.svelte";
    export let active = false;

</script>

{#if (active)}
    <div class="slide">
        <h1>MARGINAL OR MEANINGFUL?</h1>
        <h2>An immersive tool for exploring the impacts of the MBTA Communities Act</h2>
        <p>- Amelia Baum, Riccardo Fiorista, Simone Peter, Ravi Tejwani -</p>
    </div>
{/if}

<style>
    @import url("$lib/slide.css");
</style>