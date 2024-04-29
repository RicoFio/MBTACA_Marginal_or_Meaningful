<script>
    import { onMount } from "svelte";
    export let active = false;
    import * as d3 from "d3";
    import ForceGraph from "../lib/dataVisComponents/ForceGraph.svelte";
    import ForceGraphSelector from "../lib/dataVisComponents/ForceGraphSelector.svelte"

    let FirstSelectedStationName = "Coolidge Corner"
    let full_data;
    let station_data;

    let white;
    let black;
    let native;
    let asian;
    let pi;
    let other_race;
    let two_or_more;
    let hispanic;
    let male;
    let female;
    let zero;
    let one;
    let two;
    let three;
    let four; 
    let five;
    let car;
    let public_transport;
    let motorcycle;
    let bicycle;
    let walking;
    let other_mode_of_transportation;
    let work_from_home;

    onMount(async () => {
        full_data = await d3.json("/data/brookline_milton_stop_zone_zoning_usage_census_v2.geojson");
        // station_data = full_data.features.filter( (feature) => feature.properties.stop_name === "Coolidge Corner",);
    });

    // $: console.log(full_data)

    $: {
        station_data = full_data?.features.filter(
            (feature) => feature.properties.stop_name === FirstSelectedStationName,)[0];
        
        // extract demographic data by category in %
        //TODO age
        //////////////
        white = station_data?.properties.weighted_pct_not_hispanic_latino_white;
        black = station_data?.properties.weighted_pct_not_hispanic_latino_black;
        native = station_data?.properties.weighted_pct_not_hispanic_latino_native;
        asian = station_data?.properties.weighted_pct_not_hispanic_latino_asian;
        pi = station_data?.properties.weighted_pct_not_hispanic_latino_pi;
        other_race = station_data?.properties.weighted_pct_not_hispanic_latino_other;
        two_or_more = 5;
        hispanic = station_data?.properties.weighted_pct_hispanic_latino;
        // Gender
        female = station_data?.properties.weighted_pct_population_female;
        male = station_data?.properties.weighted_pct_population_male;
        // // Income
        // ///// TODO income
        // Vehicles
        zero = station_data?.properties.pct_hh_0_vehs
        one = station_data?.properties.pct_hh_1_vehs
        two = station_data?.properties.pct_hh_2_vehs
        three = station_data?.properties.pct_hh_3_vehs
        four = station_data?.properties.pct_hh_4_vehs
        five = station_data?.properties.pct_hh_5_vehs
        // Mode of transportation
        car = station_data?.properties.pct_workers_car_van
        public_transport = station_data?.properties.pct_workers_public_transportation
        motorcycle = station_data?.properties.pct_workers_motorcycle
        bicycle = station_data?.properties.pct_workers_bicycle
        walking = station_data?.properties.pct_workers_walked
        other_mode_of_transportation = station_data?.properties.pct_workers_other
        work_from_home = station_data?.properties.pct_workers_wfh
    }

    console.log("male")
    $: console.log(male)

    $: data = {
                    "age": [
                        {label: '0 to 9 years', value: 10.7},
                        {label: '9 to 17 years', value: 7.9},
                        {label: '18 to 24 years', value: 13.7},
                        {label: '25 to 34 years', value: 17.0},
                        {label: '35 to 44 years', value: 13.4},
                        {label: '45 to 54 years', value: 11.3},
                        {label: '55 to 64 years', value: 9.6},
                        {label: '65 to 74 years', value: 8.8},
                        {label: '75 to 84 years', value: 5.0},
                        {label: '85 years and over', value: 2.1},
                    ],
                    "race": [
                        {label: 'white', value: white},
                        {label: 'black', value: black},
                        {label: 'hispanic', value: hispanic},
                        {label: 'native', value: native},
                        {label: 'asian', value: asian},
                        {label: 'pi', value: pi},
                        {label: 'other_race', value: other_race},
                        {label: 'two_or_more', value: two_or_more},
                    ],
                    "gender": [
                        {label: 'male', value: male},
                        {label: 'female', value: female},
                    ],
                    "mean household income": [
                        {label: '22229 $', value: 20},
                        {label: '77063 $', value: 20},
                        {label: '132843 $', value: 20},
                        {label: '224746 $', value: 20},
                        {label: '599726 $', value: 20},
                        {label: '1099668 $', value: 5},
                    ],
                    "vehicles per household": [
                        {label: 'zero', value: zero},
                        {label: 'one', value: one},
                        {label: 'two', value: two},
                        {label: 'three', value: three},
                        {label: 'four', value: four},
                        {label: 'five', value: five},
                    ],
                    "mode of transportation": [
                        {label: 'car', value: car},
                        {label: 'public_transport', value: public_transport},
                        {label: 'motorcycle', value: motorcycle},
                        {label: 'bicycle', value: bicycle},
                        {label: 'walking', value: walking},
                        {label: 'other_mode_of_transportation', value: other_mode_of_transportation},
                        {label: 'work_from_home', value: work_from_home}
                    ]
                }
    let activeSelection = "age"
    $: current_data = data[activeSelection]
</script>

<div class="slide">
    <h1>MUNICIPALITY: Station Name</h1>
    <h2>Some explanations etc</h2>
    <p>explanations blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <p>blablabla</p>
    <h2>WHO LIVES HERE? - let's find out</h2>
    <ForceGraphSelector bind:activeSelection></ForceGraphSelector>

    {#key current_data} <!--forcing visualization to re-render when data is updated -->
    <ForceGraph
                cssHeight=50
                cssWidth=40
                data={ current_data }
                selectedCategory = { activeSelection }
            />
    {/key}
</div>

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