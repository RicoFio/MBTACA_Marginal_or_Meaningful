<script>
    // You can import graph components here if they are separate components
    // import GraphComponent from './GraphComponent.svelte';
</script>

<div class="floating-panel">
    <h1>Info</h1>
    <h1>Treemap</h1>
    <h1>Takeaway Message</h1>
</div>

<style>
    .floating-panel {
        position: fixed;
        left: 5%;
        top: 50%;  /* Center the panel vertically */
        transform: translateY(-50%);
        width: 300px;  /* Adjust the width as necessary */
        background: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        border-radius: 5px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;  /* Space between graphs */
        z-index: 1000;  /* Make sure it floats above other content */
        grid-template-columns: auto auto; /* Define two columns */
        grid-auto-rows: auto; /* This will create a new row for each term/description pair */
        align-items: start;
        background-color: rgba(10, 0, 0, 0.4); /* Semi-transparent background */
        backdrop-filter: blur(10px);
        font-size: 0.9em;
        transition-duration: 500ms;
        transition-property: opacity, visibility;

        font-family: 'Montserrat', sans-serif;
        visibility: visible;
        color: #a9987a;
    }

    .graph {
        height: 200px;  /* Adjust based on your needs */
        background-color: #f0f0f0;  /* A light grey background to distinguish the graph area */
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #ccc;  /* Optional border for graph boxes */
    }
</style>
