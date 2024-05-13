<script>
    import {loadStationZoningAndUsageDataDict} from "./../lib/dataVisComponents/zoningData"

    export let active = false;
    export let value;
    export let municipality;
    export let stations;
    export let comparisonMode;
    export let zoningAndCensusFiles;


    $: firstStation = (stations?.length > 0) ? stations[0] : undefined;
    $: secondStation = (stations?.length > 1) ? stations[1] : undefined;
    let firstStationData;
    let secondStationData;
    let oldFirstStation;
    let oldSecondStation;
    let maxIndex;

    $: {
        console.log("stations");
        console.log(stations);
        console.log("firstStation");
        console.log(firstStation);
        console.log("secondStation");
        console.log(secondStation);
    }

    $: {
        if (active) {
            comparisonMode = true;
        }
    }

    $: firstStation, (async () => {
        if (firstStation !== undefined && firstStation?.Name !== oldFirstStation?.Name) {
            firstStationData = await loadStationZoningAndUsageDataDict(zoningAndCensusFiles, firstStation);
            oldFirstStation = firstStation;
            console.log("ENTEREEEEED Station 1!");
            console.log("zoning test", firstStationData);
        }
    })();

    $: secondStation, (async () => {
        if (secondStation !== undefined && secondStation?.Name !== oldSecondStation?.Name) {
            secondStationData = await loadStationZoningAndUsageDataDict(zoningAndCensusFiles, secondStation);
            oldSecondStation = secondStation;
            console.log("ENTEREEEEED Station 2!")
            console.log("zoning test", secondStationData)
        }
    })();

    function calculate_max_age(stationData) {
        let value_1 = parseFloat(stationData?.percentage_weighted_total_population_male_under_18_years) + parseFloat(stationData?.percentage_weighted_total_population_female_under_18_years)
        let value_2 = parseFloat(stationData?.percentage_weighted_total_population_male_18_to_34_years) + parseFloat(stationData?.percentage_weighted_total_population_female_18_to_34_years)
        let value_3 = parseFloat(stationData?.percentage_weighted_total_population_male_35_to_64_years) + parseFloat(stationData?.percentage_weighted_total_population_female_35_to_64_years)
        let value_4 = parseFloat(stationData?.percentage_weighted_total_population_male_65_years_and_over) + parseFloat(stationData?.percentage_weighted_total_population_female_65_years_and_over)

        let values = [value_1, value_2, value_3, value_4]

        maxIndex = values.indexOf(Math.max(...values));

        if (maxIndex == 0) {
            maxIndex = 'under 18 years'
        } else if (maxIndex == 1) {
            maxIndex = '18 to 34 years'
        } else if (maxIndex == 2) {
            maxIndex = '35 to 64 years'
        } else {
            maxIndex = 'over 65 years'
        }
        return maxIndex
    }

    function calculate_max_transport(stationData) {
        let value_1 = parseFloat(stationData?.percentage_weighted_workers_16_years_and_over_car_truck_or_van)
        let value_2 = parseFloat(stationData?.percentage_weighted_workers_16_years_and_over_public_transportation_includes_taxicab)
        let value_3 = parseFloat(stationData?.percentage_weighted_workers_16_years_and_over_motorcycle)
        let value_4 = parseFloat(stationData?.percentage_weighted_workers_16_years_and_over_bicycle)
        let value_5 = parseFloat(stationData?.percentage_weighted_workers_16_years_and_over_walked)
        let value_6 = parseFloat(stationData?.percentage_weighted_workers_16_years_and_over_other_means)
        let value_7 = parseFloat(stationData?.percentage_weighted_workers_16_years_and_over_worked_at_home)

        let values = [value_1, value_2, value_3, value_4, value_5, value_6, value_7]

        maxIndex = values.indexOf(Math.max(...values));

        if (maxIndex == 0) {
            maxIndex = 'car'
        } else if (maxIndex == 1) {
            maxIndex = 'public transport'
        } else if (maxIndex == 2) {
            maxIndex = 'motorcycle'
        } else if (maxIndex == 3) {
            maxIndex = 'bicycle'
        } else if (maxIndex == 4) {
            maxIndex = 'walking'
        } else if (maxIndex == 5) {
            maxIndex = 'other modes of transport'
        } else {
            maxIndex = 'working from home'
        }
        return maxIndex
    }

    function cars_per_household(stationData) {
        let average_cars = (parseFloat(stationData?.percentage_weighted_occupied_housing_units_no_vehicle_available) * 0 +
            parseFloat(stationData?.percentage_weighted_occupied_housing_units_1_vehicle_available) * 1 +
            parseFloat(stationData?.percentage_weighted_occupied_housing_units_2_vehicles_available) * 2 +
            (1 - parseFloat(stationData?.percentage_weighted_occupied_housing_units_no_vehicle_available) -
                parseFloat(stationData?.percentage_weighted_occupied_housing_units_1_vehicle_available) -
                parseFloat(stationData?.percentage_weighted_occupied_housing_units_2_vehicles_available)) * 3)

        return parseFloat(average_cars).toFixed(2)
    }

</script>

<div class="slide">
    {#if (municipality && !firstStation)}
        <h1>Select a station in {municipality?.Name}</h1>
    {:else if (municipality && firstStation && !secondStation)}
        <h1>Select a second station in {municipality?.Name}</h1>
    {:else}
        <h1>Let's consider {firstStation?.Name} and {secondStation?.Name} in {municipality?.Name}</h1>
        <p>
            Now we compare their zoning, usage, and demographics. The effects of creating a multifamily district near
            each zone may be disparate or similar. Use this information to determine where a multi-family district
            siting would be most reasonable for your selected community.
        </p>
        <br>

        <table>
            <caption>Demographic breakdown</caption>
            <thead>
            <tr>
                <th>Category</th>
                <th>{firstStation?.Name}</th>
                <th>{secondStation?.Name}</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>Main age group</td>
                <td>{calculate_max_age(firstStationData)}</td>
                <td>{calculate_max_age(secondStationData)}</td>
            </tr>
            <tr>
                <td>Median household income [$]</td>
                <td>{String(firstStationData?.weighted_median_household_income_in_2022_inflation_adjusted_dollars)}</td>
                <td>{String(secondStationData?.weighted_median_household_income_in_2022_inflation_adjusted_dollars)}</td>
            </tr>
            <tr>
                <td>Average cars per household</td>
                <td>{cars_per_household(firstStationData)}</td>
                <td>{cars_per_household(secondStationData)}</td>
            </tr>
            <tr>
                <td>Preferred mode of transport</td>
                <td>{calculate_max_transport(firstStationData)}</td>
                <td>{calculate_max_transport(secondStationData)}</td>
            </tr>
            </tbody>
        </table>

        <p>
            In the area surrounding {firstStation?.Name}, there are
            currently {String(firstStationData?.pctZonedAsSF).slice(0, 5)}% parcels zoned for single family residency,
            of which {String(firstStationData?.pctUsedAsSF).slice(0, 5)}% are actually used as Single Family. This means
            that {String(firstStationData?.pctMustUpzone).slice(0, 5)}% parcels (colored in orange) must upzone in order
            to comply with the MBTA communities Act, and {String(firstStationData?.pctWillChange).slice(0, 5)}% will
            likely actually change their use.
        </p>
        <p>
            In comparison, in the area surrounding {secondStation?.Name}, there are
            currently {String(secondStationData?.pctZonedAsSF).slice(0, 5)}% parcels zoned for single-family residency,
            of which {String(secondStationData?.pctUsedAsSF).slice(0, 5)}% as used as Single Family. This means
            that {String(secondStationData?.pctMustUpzone).slice(0, 5)}% parcels (colored in orange) must upzone to
            comply with the MBTA communities Act, and {String(secondStationData?.pctWillChange).slice(0, 5)}% will
            likely actually change their use.
        </p>
    {/if}
</div>

<style>
    @import url("$lib/slide.css");

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th, td {
        border: 1px solid #ccc;
        padding: 8px;
        text-align: left;
    }

    caption {
        font-size: 1.0em;
        margin: 10px 0;
    }
</style>
