<script>
    export let active = false;
    export let absolute_slide_value = 0;

    let entered = 0;
    $: if (active && entered == 0) {
        absolute_slide_value = 0;
        entered += 1;
    }
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