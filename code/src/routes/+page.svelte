<script>
    import mapboxgl from "mapbox-gl";
    import * as d3 from 'd3';
    import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    import {onMount} from "svelte";
    import buffer from '@turf/buffer';
    import { point } from '@turf/helpers';

    import BaseMap from "$lib/mapComponents/BaseMap.svelte";
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";

    mapboxgl.accessToken = "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";

    let baseMap;
    let stations = [];
    let bounds = [];
    let mapViewChanged = 0;
    let query = "";
    let municipalities = [];
    let municipalitiesFilter = -1;
    let filteredStations = [];
    let input = "";
    let suggestions = [];
    let selectedStationIdxs = [];
    let municipalitySelected = false;

    onMount(async () => {
        municipalities = await d3.json("/data/mbta_municipalities.geojson");
        stations = await d3.json("/data/mbta_community_stops.geojson");

        stations = stations.features.map(station => {
            let newStation = {};
            newStation.Lat = station.geometry.coordinates[1];
            newStation.Long = station.geometry.coordinates[0];
            newStation.WithBuffer = buffer(point([newStation.Long, newStation.Lat]), 0.5, {units: 'miles'}).geometry.coordinates[0];
            newStation.Community = station.properties.community;
            newStation.Name = station.properties.stop_name;
            newStation.Routes = station.properties.routes;
            newStation.RouteColors = station.properties.route_colors;
            newStation.Type = station.properties.mbta_comm_type;
            return newStation;
        });

        municipalities = municipalities.features.map(municipality => {
            let newMunicipality = {};
            newMunicipality.Geometries = {};

            if (municipality.geometry && Array.isArray(municipality.geometry.coordinates[0])) {
                newMunicipality.Geometries = municipality.geometry;
            } else {
            }
            newMunicipality.Name = municipality.properties.community;
            newMunicipality.TotalHousingUnits = municipality.properties.housing_units_2020;
            newMunicipality.PopulationSize = municipality.properties.pop2020;
            newMunicipality.MBTACommunityType = municipality.properties.mbta_comm_type;
            newMunicipality.MinHousingCapacityRequirement = municipality.properties.min_rf1_cap_req;
            return newMunicipality;
        })
    })

    // Reactive statement to update suggestions based on input
    $: if (input) {
        suggestions = municipalities.filter(m =>
            m.Name && typeof m.Name === 'string' && m.Name.toLowerCase().startsWith(input.toLowerCase())
        );
    } else {
        suggestions = [];
    }

    function selectSuggestion(suggestion) {
        query = suggestion.Name; // Set the query to the selected municipality name
        suggestions = []; // Clear suggestions

        // Calculate the bounding box of the selected municipality
        bounds = calculateBoundingBox(suggestion.Geometries);

        baseMap.fitBounds(bounds, { padding: 20 });
    }

    $: filteredMunicipalities = query ?
        municipalities.filter(m =>
            m.Name && typeof m.Name === 'string' &&
            m.Name.toLowerCase().includes(query.toLowerCase())
        ) :
        municipalities;

    $: municipalitySelected = !!query

    $: {
        if (query && !!selectedStationIdxs) {
            filteredStations = stations.filter(m =>
                m.Community && typeof m.Community === 'string' &&
                m.Community.toLowerCase().includes(query.toLowerCase())
            );
            // filteredStations = filteredStations.map(station => {
            //     let newStation = {...station};
            //     newStation.WithBuffer = buffer(point([newStation.Long, newStation.Lat]), 0.1, {units: 'miles'}).geometry.coordinates[0];
            //     return newStation;
            // });
        } else {
            filteredStations = stations;
        }
    }

</script>

<!--TODO replace with https://github.com/rob-balfre/svelte-select?tab=readme-ov-file component-->
<div>
    <h1>Search</h1>
    <input type="search" bind:value={input}
           aria-label="Municipality search" placeholder="🔍 Find your municipality" />
</div>
<div>
    {#if suggestions.length}
        <ul>
            {#each suggestions as suggestion}
                <li on:click={() => selectSuggestion(suggestion)}>
                    {suggestion.Name}
                </li>
            {/each}
        </ul>
    {/if}
</div>

<br>
<BaseMap
        class="baseMap"
        bind:this={baseMap}
        bind:municipalities={filteredMunicipalities}
        bind:stations={filteredStations}
        bind:selectedStationIdxs={selectedStationIdxs}
        bind:municipalitySelected={municipalitySelected}
/>

<style>
    @import url("$lib/global.css");
</style>
