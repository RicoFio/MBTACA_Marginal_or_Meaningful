<script>
    import Select from 'svelte-select';
    export let active = false;

    export let guidedMode, comparisonMode, explorationMode;

    function handleExploreButton(e) {
        console.log("CALLING")
        guidedMode = false;
        comparisonMode = false;
        explorationMode = true;
    }
</script>

<div class="slide">
    <button class="explore-button" on:click={handleExploreButton}>
        EXPLORE NOW
    </button>
</div>

<style>
    @import url("$lib/slide.css");

    .explore-button {
        background-color: white;  /* White background */
        color: black;             /* Text color */
        border: none;             /* No border */
        padding: 10px 20px;       /* Padding around the text */
        font-size: 16px;          /* Text size */
        font-weight: bold;        /* Font weight */
        border-radius: 25px;      /* Rounded corners */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Shadow for 3D effect */
        transition: all 0.3s;     /* Smooth transition for mouse events */
        cursor: pointer;          /* Pointer cursor on hover */
        outline: none;            /* Remove outline on focus */
    }

    .explore-button:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.15); /* Enhanced shadow on hover */
        transform: translateY(-2px); /* Slight raise on hover */
    }

    .explore-button:active {
        box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* Smaller shadow on click */
        transform: translateY(1px); /* Slight press down on click */
    }
</style>