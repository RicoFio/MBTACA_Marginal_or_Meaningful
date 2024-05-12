<script>

    import Scrolly from "../panelComponents/Scrolly.svelte";
    import Slide1 from "../../slides/Slide1.svelte";
    import Slide11 from "../../slides/Slide1.1.svelte";
    import Slide12 from "../../slides/Slide1.2.svelte";
    import Slide2 from "../../slides/Slide2.svelte";
    import Slide21 from "../../slides/Slide2.1.svelte";
    import Slide3 from "../../slides/Slide3.svelte";
    import Slide4 from "../../slides/Slide4.svelte";
    import Slide5 from "../../slides/Slide5.svelte";
    import Slide6 from "../../slides/Slide6.svelte";
    import { tick } from "svelte";
    import { onMount } from 'svelte';

    let ready = false;

    export let value = 0;
    export let municipalities;
    export let stations;
    export let selectedMunicipality;
    export let selectedStations;
    export let guidedMode;
    export let reset_scroll = false;
    export let absolute_slide_value;

    let visibility_slide12 = false;
    let visibility_slide21 = false;
    let visibility_slide4 = false;
    let visibility_slide5 = false;
    let isVisibleSecond_slide12 = false;
    let isVisible_slide12 = false;
    $: isVisible_slide1 = false;

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

    $: if (reset_scroll) {
        console.log("rest button")
        scrollToSlide(0)
    }

    onMount(() => {
      if (scrollyComponent) {
          ready = true;
      }
    });

    // Default to true to show Slide2 initially
    let isSlide2Active = false;
    console.log("isSlide2Active", isSlide2Active)
    let isSlide1Active = 'value === 0';

    // $: if (isVisible_slide12 == true) {
    //     console.log("HERETEW")
    //     value = 2;
    // }

    // $: if (isSlide2Active && value == 2) {
    //     value = 3;
    // }

    // Reactive statement to handle changes in selectedMunicipality
    let check_if_entered = 0;
    $: if (isVisibleSecond_slide12 == true && check_if_entered == 0) {
        console.log("is visible", isVisibleSecond_slide12)
        isSlide2Active = 'value === 3';
        console.log("slide 2 is now active", isSlide2Active)
        check_if_entered += 1;
    }
    $: if (ready && selectedMunicipality) {
        console.log("Selected Municipality is set", selectedMunicipality);
        visibility_slide21 = 'value === 4';
        let value_scroll = 6; // Assuming this is the index for Slide21
        // isSlide1Active = true;
        scrollToNextSlide(value_scroll, () => {
            // This callback is called after the scrolling animation completes
            isSlide2Active = false;
            console.log("Slide2 is now inactive.", isSlide2Active);
        });
        isSlide1Active = 'value === 0';
    } 
    else {
        console.log("Selected Municipality is not set");
    }

    $: if (ready && firstStation) {
        console.log("Selected station is set")
        visibility_slide4 = 'value === 5'
        let value_scroll_station = 4;
        scrollToSlide(value_scroll_station)
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

    function scrollToNextSlide(slideIndex, callback) {
        console.log("Scrolling to next slide called", slideIndex+1);
        if (scrollyComponent && scrollyComponent.scrollToIndex) {
            scrollyComponent.scrollToIndex(slideIndex+1);
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

$: absolute_slide_value = 0;
$: if (absolute_slide_value) {
    console.log("ABSOLUT test", absolute_slide_value)
}

let check_entered = 0;
$: if (isVisible_slide1 && check_entered == 0 && value == 1) {
    console.log("YEEEEH")
      console.log(visibility_slide12)
      visibility_slide12 = true;
    //   value = 2;
      console.log("Slide12 is now")
      console.log(visibility_slide12)
      console.log("value", value)
      check_entered += 1;
    }
    

</script>

<div class="panel" style="position: absolute; top: 0; left: 0; width: 40%; height: 100%; background-color: rgba(0, 0, 0, 0.7); padding: 20px; color: {colors[3]}; backdrop-filter: blur(8px);">
    <Scrolly bind:this={scrollyComponent} bind:value bind:absolute_slide_value> <!-- 3. This is what updates value -->
        <!-- {#each ['MARGINAL', 'OR', 'World!'] as text, i}
            <div class="step" class:active={value === i}>
                <p>{text}</p> 
            </div>
        {/each} -->
        <Slide1 active={isSlide1Active} bind:value bind:absolute_slide_value/>
        <Slide11 active={value === 1} bind:value bind:absolute_slide_value bind:isVisible_slide1={isVisible_slide1}/>
        <Slide12 active={visibility_slide12} bind:value bind:isVisibleSecond_slide12={isVisibleSecond_slide12} bind:isVisible_slide12={isVisible_slide12} bind:absolute_slide_value />
        <Slide2 active={isSlide2Active} bind:value bind:municipalities={municipalities} bind:selectedMunicipality={selectedMunicipality} bind:absolute_slide_value/>
        <Slide21 active={visibility_slide21} bind:value bind:municipality={selectedMunicipality} bind:station={firstStation} bind:absolute_slide_value/>
        <!-- <Slide3 active={value === 4}  bind:municipality={selectedMunicipality} bind:station={firstStation}/> -->
        <Slide4 active={visibility_slide4} bind:value bind:municipality={selectedMunicipality} bind:station={firstStation} bind:visibility_slide5={visibility_slide5} bind:absolute_slide_value/>
        <Slide5 active={visibility_slide5}  bind:value bind:municipality={selectedMunicipality} bind:station={firstStation} bind:absolute_slide_value/>
        <Slide6 active={value === 7} bind:value bind:absolute_slide_value />
    </Scrolly>
</div>

<style>
    @import url("$lib/global.css");

    div {
        z-index: 5;
        text-align: center;
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

    .panel {
    position: relative; /* Confirms the panel is the positioned ancestor */
    overflow-y: auto;  /* Allows vertical scrolling */
    overflow-x: hidden; /* Disables horizontal scrolling */
    width: 40%; /* Adjust as necessary */
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    color: var(--color); /* Use CSS variables for better management */
    display: flex;
    flex-direction: row; /* Makes the children lay out in a row */
}

</style>

  