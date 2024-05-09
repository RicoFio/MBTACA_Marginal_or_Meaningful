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
    import { tick } from "svelte";
    import { onMount } from 'svelte';

    let ready = false;

    let value = 0;
    export let municipalities;
    export let stations;
    export let selectedMunicipality;
    export let selectedStations;
    export let guidedMode;

    let container;
    // $: console.log({ value });
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

    export let scrollyComponent;

    onMount(() => {
      if (scrollyComponent) {
          ready = true;
      }
    });

    // Default to true to show Slide2 initially
    let isSlide2Active = 'value === 2';
    let isSlide1Active = 'value === 0';

    // Reactive statement to handle changes in selectedMunicipality
    $: if (ready && selectedMunicipality) {
        console.log("Selected Municipality is set", selectedMunicipality);
        let value_scroll = 4; // Assuming this is the index for Slide21
        // isSlide1Active = true;
        scrollToSlide(value_scroll, () => {
            // This callback is called after the scrolling animation completes
            isSlide2Active = false;
            console.log("Slide2 is now inactive.");
        });
        isSlide1Active = 'value === 0';
    } else {
        console.log("Selected Municipality is not set");
    }

    // Reactive statement to handle changes
    // $: if (scrollyComponent) {
      // Logic to move to the next slide, ensuring it does not exceed total slides
    //   value = (value + 1) % 8; // Replace 'slides.length' with your total number of slides
    //   scrollToSlide(value);
    //   scrollyComponent = 0;
    // }

    // Function to scroll to a particular slide
    function scrollToSlide(slideIndex, callback) {
        console.log("Scrolling to slide called", slideIndex);
        if (scrollyComponent && scrollyComponent.scrollToIndex) {
            scrollyComponent.scrollToIndex(slideIndex);
            if (callback) {
                // Assuming scrollIntoView is not returning a Promise, we simulate callback execution
                // after a set time that you estimate as the scroll duration
                setTimeout(callback, 110); // adjust time based on your scroll duration
            }
        } else {
            console.log('scrollToIndex method is undefined');
            if (callback) {
                callback();
            }
        }
    }

    $: console.log('Current slide index (value):', value);

    // let value_slide2;
    // $: {
    //     if (!selectedMunicipality) {
    //         value_slide2 = 2;
    //     }
    //     else {
    //         value_slide2 = false;
    //     }
    // }
    // $: showSlides = {
    //     S1: false,
    //     S11: false,
    //     S2: false,
    //     S21: false,
    //     S3: false,
    //     S4: false,
    //     S6: false,
    // }

    

</script>

<div class="panel" style="position: absolute; top: 0; left: 0; width: 40%; height: 100%; background-color: rgba(0, 0, 0, 0.6); padding: 20px; color: {colors[3]};">
    <Scrolly bind:this={scrollyComponent} bind:value> <!-- 3. This is what updates value -->
        <!-- {#each ['MARGINAL', 'OR', 'World!'] as text, i}
            <div class="step" class:active={value === i}>
                <p>{text}</p> 
            </div>
        {/each} -->
        <Slide1 active={isSlide1Active} />
        <Slide11 active={value === 1} />
        <Slide2 active={isSlide2Active}  bind:municipalities={municipalities} bind:selectedMunicipality={selectedMunicipality}/>
        <Slide21 active={value === 3} bind:municipality={selectedMunicipality} bind:station={firstStation} bind:value/>
        <!-- <Slide3 active={value === 4}  bind:municipality={selectedMunicipality} bind:station={firstStation}/> -->
        <Slide4 active={value === 4}  bind:municipality={selectedMunicipality} bind:station={firstStation}/>
        <Slide5 active={value === 5}  bind:municipality={selectedMunicipality} bind:station={firstStation}/>
        <Slide6 active={value === 6} />
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

  