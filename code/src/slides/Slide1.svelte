<script>
    export let active = false;

</script>

{#if (active)}
    <div class="slide">
        <h1>MARGINAL OR MEANINGFUL?</h1>
        <h2>An immersive tool for exploring the impacts of the MBTA Communities Act</h2>
         <h3>- Amelia Baum, Riccardo Fiorista, Simone Peter, Ravi Tejwani - </h3>
        <br>
        <br>
        <div class="scroll-indicator"></div>
    </div>
{/if}

<style>
    @import url("$lib/slide.css");

    .slide .scroll-indicator {
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 15px solid white; /* Adjust color to match your slide's theme */
    margin: 20px auto; /* Centers the arrow and adds space above it */
    animation: bounce 2s infinite; /* Adds a bouncing animation to catch attention */
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-20px);
    }
    60% {
        transform: translateY(-10px);
    }
}

</style>