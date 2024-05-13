<script>
    import {onMount} from "svelte";
    import * as d3 from "d3";
    import ForceGraph from "../lib/dataVisComponents/ForceGraph.svelte";
    import ForceGraphSelector from "../lib/dataVisComponents/ForceGraphSelector.svelte"
    import {observerStore} from '../lib/panelComponents/Scrolly_slide.js';

    export let active = false;

    export let municipality = {};
    export let station = {};

    let full_data;
    let station_data;

    let under_18 = 0;
    let to_34 = 0;
    let to_64 = 0;
    let over_65 = 0;
    let less_than_25000 = 0;
    let to_49999 = 0;
    let to_74999 = 0;
    let to_99999 = 0;
    let more_than_100000 = 0;
    let white = 0;
    let black = 0;
    let asian = 0;
    let other_race = 0;
    let hispanic = 0;
    let male = 0;
    let female = 0;
    let zero = 0;
    let one = 0;
    let two = 0;
    let three_or_more = 0;
    let car = 0;
    let public_transport = 0;
    let motorcycle = 0;
    let bicycle = 0;
    let walking = 0;
    let other_mode_of_transportation = 0;
    let work_from_home = 0;

    let isVisible = false;
    observerStore.subscribe(store => {
        isVisible = store.isVisible;
    });

    export let value;
    $: if (value === 6) {
        observerStore.resetVisibility();  // Reset visibility whenever checking this condition
        observerStore.startObservation();
    }

    onMount(async () => {
        full_data = await d3.json("/data/mbta_community_stops_with_buffer_and_census.geojson");
        // station_data = full_data.features.filter( (feature) => feature.properties.stop_name === "Coolidge Corner",);
    });


    $: {
        station_data = full_data?.features.filter(
            (feature) => feature.properties.stop_name === station?.Name,)[0];

        // extract demographic data by category in %
        // age
        under_18 = (station_data?.properties.percentage_weighted_total_population_male_under_18_years + station_data?.properties.percentage_weighted_total_population_female_under_18_years) * 100;
        to_34 = (station_data?.properties.percentage_weighted_total_population_male_18_to_34_years + station_data?.properties.percentage_weighted_total_population_female_18_to_34_years) * 100;
        to_64 = (station_data?.properties.percentage_weighted_total_population_male_35_to_64_years + station_data?.properties.percentage_weighted_total_population_female_35_to_64_years) * 100;
        over_65 = (station_data?.properties.percentage_weighted_total_population_male_65_years_and_over + station_data?.properties.percentage_weighted_total_population_female_65_years_and_over) * 100;
        // race
        white = (station_data?.properties.percentage_weighted_total_population_not_hispanic_or_latino_white_alone) * 100;
        black = (station_data?.properties.percentage_weighted_total_population_not_hispanic_or_latino_black_or_african_american_alone) * 100;
        asian = (station_data?.properties.percentage_weighted_total_population_not_hispanic_or_latino_asian_alone) * 100;
        other_race = (station_data?.properties.percentage_weighted_total_population_not_hispanic_or_latino_american_indian_and_alaska_native_alone + station_data?.properties.percentage_weighted_total_population_not_hispanic_or_latino_native_hawaiian_and_other_pacific_islander_alone + station_data?.properties.percentage_weighted_total_population_not_hispanic_or_latino_some_other_race_alone + station_data?.properties.percentage_weighted_total_population_not_hispanic_or_latino_two_or_more_races) * 100;
        hispanic = (station_data?.properties.percentage_weighted_total_population_hispanic_or_latino) * 100;
        // Gender
        female = (station_data?.properties.percentage_weighted_total_population_female) * 100;
        male = (station_data?.properties.percentage_weighted_total_population_male) * 100;
        // Income
        less_than_25000 = station_data?.properties.percentage_weighted_households_less_than_25000 * 100;
        to_49999 = station_data?.properties.percentage_weighted_households_25000_to_49999 * 100;
        to_74999 = station_data?.properties.percentage_weighted_households_50000_to_74999 * 100;
        to_99999 = station_data?.properties.percentage_weighted_households_75000_to_99999 * 100;
        more_than_100000 = station_data?.properties.percentage_weighted_households_100000_or_more * 100;
        // Vehicles
        zero = station_data?.properties.percentage_weighted_occupied_housing_units_no_vehicle_available * 100;
        one = station_data?.properties.percentage_weighted_occupied_housing_units_1_vehicle_available * 100;
        two = station_data?.properties.percentage_weighted_occupied_housing_units_2_vehicles_available * 100;
        three_or_more = 100 - zero - one - two;
        // Mode of transportation
        car = station_data?.properties.percentage_weighted_workers_16_years_and_over_car_truck_or_van * 100;
        public_transport = station_data?.properties.percentage_weighted_workers_16_years_and_over_public_transportation_includes_taxicab * 100;
        motorcycle = station_data?.properties.percentage_weighted_workers_16_years_and_over_motorcycle * 100;
        bicycle = station_data?.properties.percentage_weighted_workers_16_years_and_over_bicycle * 100;
        walking = station_data?.properties.percentage_weighted_workers_16_years_and_over_walked * 100;
        other_mode_of_transportation = station_data?.properties.percentage_weighted_workers_16_years_and_over_other_means * 100;
        work_from_home = station_data?.properties.percentage_weighted_workers_16_years_and_over_worked_at_home * 100;
    }

    $: data = {
        "age": [
            {label: 'under 18 years', value: under_18},
            {label: '18 to 34 years', value: to_34},
            {label: '35 to 64 years', value: to_64},
            {label: 'over 65 years', value: over_65},
        ],
        "race": [
            {label: 'white', value: white},
            {label: 'black', value: black},
            {label: 'hispanic', value: hispanic},
            {label: 'asian', value: asian},
            {label: 'other_race', value: other_race},
        ],
        "gender": [
            {label: 'male', value: male},
            {label: 'female', value: female},
        ],
        "median household income": [
            {label: 'less than 25,000 $', value: less_than_25000},
            {label: '25,000 to 49,999 $', value: to_49999},
            {label: '50,000 to 74,999 $', value: to_74999},
            {label: '75,000 to 99,999 $', value: to_99999},
            {label: 'more than 100,000 $', value: more_than_100000},
        ],
        "vehicles per household": [
            {label: 'zero', value: zero},
            {label: 'one', value: one},
            {label: 'two', value: two},
            {label: 'three or more', value: three_or_more},
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
    $: current_data = data[activeSelection];
</script>
<!-- <ScrollySlide bind:value expectedValue={5}> -->
<div class="slide">
    {#if (municipality && station)}
        <h1>{municipality.Name}: {station.Name}</h1>
        <p>
            {station.Name} is located within {municipality.Name}, a {municipality.MBTACommunityType} community. It
            serves the following routes: {station.Routes}. The MBTA Communities Act stipulates that municipalities must
            create at least one by-right multifamily district within a 0.5-mile radius of a transit stop within their
            borders, which is visualized on the right. <br> <br>
            Toggle the force diagrams to see relevant demographic statistics for the zone around the transit station.
            Racial, age, gender and income demographics, as well as behavioral characteristics like how much of the
            population uses transit to get to work, may influence the effect of upzoning on a certain location.
            <br>
            <br>
        </p>
    {/if}
    <h2>WHO LIVES HERE? - let's find out</h2>
    <ForceGraphSelector bind:activeSelection></ForceGraphSelector>

    {#key current_data} <!--forcing visualization to re-render when data is updated -->
        {#if !isNaN(under_18)}
            <ForceGraph
                    cssHeight=50
                    cssWidth=40
                    data={ current_data }
                    selectedCategory={ activeSelection }
            />
        {/if}
    {/key}
</div>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<!-- </ScrollySlide> -->

<style>
    @import url("$lib/slide.css");

    p {
        margin: 0;
        padding: 1em;
        width: 100%;
        text-align: center;
    }
</style>
