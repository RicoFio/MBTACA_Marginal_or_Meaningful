<script>
    import Select from 'svelte-select';
    export let active = false;
    export let absolute_slide_value;

    let entered = 0;
    if (active && entered == 0 && absolute_slide_value == 6) {
        console.log("LAST SLIDE ENTERED")
        absolute_slide_value = 7;
        entered += 1;
    }

</script>

<div class="slide">
    <h1>TO BE CONTINUED ...</h1>
    <h2>
        What you will find here soon:
    </h2>
    <ul>
        <li>The ability to compare two stations</li>
        <li>The ability to explore the map on your own</li>
    </ul>
    <h1>Made with ❤️</h1>
</div>

<style>
    @import url("$lib/slide.css");
</style>
