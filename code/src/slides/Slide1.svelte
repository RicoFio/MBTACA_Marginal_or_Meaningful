<script>
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