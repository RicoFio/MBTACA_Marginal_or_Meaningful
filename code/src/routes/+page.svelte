<script>
    import mapboxgl from "mapbox-gl";
    import * as d3 from 'd3';
    import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    import {onMount} from "svelte";
    import buffer from '@turf/buffer';
    import { point } from '@turf/helpers';
    // import ForceGraphTest from "../lib/dataVisComponents/ForceGraph.svelte";
    // import ForceGraphSelector from "../lib/dataVisComponents/ForceGraphSelector.svelte"
    import PanelComponent from '../lib/dataVisComponents/panel.svelte';

    import BaseMap from "$lib/mapComponents/BaseMap.svelte";
    import {calculateBoundingBox} from "$lib/mapComponents/mapUtils.js";

    mapboxgl.accessToken = "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";

    let baseMap;
    let stations = [];
    let parcelFiles = [];
    let bounds = [];
    let mapViewChanged = 0;
    let searchItems;
    let searchSelectedMunicipality;
    let selectedMunicipality;
    let query = "";
    let municipalities = [];
    let municipalitiesFilter = -1;
    // let filteredStations = [];
    let input = "";
    let suggestions = [];
    let selectedStations = [];
    let municipalitySelected = false;
    let guidedMode = true;

    // $: console.log(parcelFiles);

    onMount(async () => {
        municipalities = await d3.json("/data/mbta_municipalities.geojson");
        stations = await d3.json("/data/mbta_community_stops.geojson");
        parcelFiles = await d3.csv("/data/parcels/per_station/file_name_reference.csv");

        stations = stations.features.map(station => {
            let newStation = {
                Lat: station.geometry.coordinates[1],
                Long: station.geometry.coordinates[0],
                Community: station.properties.community,
                Name: station.properties.stop_name,
                Routes: station.properties.routes,
                RouteColors: station.properties.route_colors,
                Type: station.properties.mbta_comm_type,
                getBuffer: function(radius) {
                    return buffer(point([this.Long, this.Lat]), radius, { units: 'miles' }).geometry.coordinates[0];
                }
            };

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

    $: if (searchSelectedMunicipality) {
        selectedMunicipality = municipalities.filter(m => {
            return m.Name == searchSelectedMunicipality;
        })[0];
        bounds = calculateBoundingBox(selectedMunicipality?.Geometries);
        baseMap.fitBounds(bounds, {padding: 20});
    }

    $: filteredMunicipalities = query ?
        municipalities.filter(m =>
            m.Name && typeof m.Name === 'string' &&
            m.Name.toLowerCase().includes(query.toLowerCase())
        ) :
        municipalities;

    $: municipalitySelected = !!query

    $: firstSelectedStationName = selectedStations[0]?.Name;

    // $: {
    //     if (selectedMunicipality && !!selectedStations) {
    //         filteredStations = stations.filter(m =>
    //             m.Community && typeof m.Community === 'string' &&
    //             m.Community.toLowerCase().includes(selectedMunicipality?.Name.toLowerCase())
    //         );
    //         filteredStations = filteredStations.map(station => {
    //             let newStation = {...station};
    //             let factor = firstSelectedStationName && newStation.Name == firstSelectedStationName ? 0.5 : 0.1
    //             newStation.WithBuffer = buffer(point([newStation.Long, newStation.Lat]), factor, {units: 'miles'}).geometry.coordinates[0];
    //             return newStation;
    //         });
    //     } else {
    //         filteredStations = stations;
    //     }
    // }

    // $: {
    //     if (firstSelectedStationName) {
    //         filteredStations = filteredStations.map(station => {
    //             let newStation = {...station};
    //             let factor = newStation.Name == firstSelectedStationName ? 0.5 : 0.1
    //             newStation.WithBuffer = buffer(point([newStation.Long, newStation.Lat]), factor, {units: 'miles'}).geometry.coordinates[0];
    //             return newStation;
    //         });
    //     }
    // }

    const data = {
                    "age": [
                        {label: 'age group 1', value: 20},
                        {label: 'age group 2', value: 80},
                        {label: 'age group 3', value: 40},
                    ],
                    "race": [
                        {label: 'race group 1', value: 30},
                        {label: 'race group 2', value: 60},
                        {label: 'race group 3', value: 50},
                    ],
                    "gender": [
                        {label: 'male', value: 50},
                        {label: 'female', value: 90},
                    ],
                    "income": [
                        {label: 'income group 1', value: 80},
                        {label: 'income group 2', value: 20},
                        {label: 'income group 3', value: 40},
                        {label: 'income group 4', value: 50},
                    ],
                    "cars per household": [
                        {label: 'none', value: 20},
                        {label: 'one', value: 50},
                        {label: 'two or more', value: 90},
                    ],
                    "mode of transit/work commute": [
                        {label: 'car', value: 90},
                        {label: 'train', value: 60},
                        {label: 'bike', value: 20},
                        {label: 'walk', value: 10},
                        {label: 'other', value: 10}
                    ]
                }
    let activeSelection = "mode of transit/work commute"

    $: current_data = data[activeSelection]

</script>

<!--TODO replace with https://github.com/rob-balfre/svelte-select?tab=readme-ov-file component-->
<BaseMap
        class="baseMap"
        bind:this={baseMap}
        bind:municipalities={filteredMunicipalities}
        bind:stations={stations}
        bind:selectedStations={selectedStations}
        bind:selectedMunicipality={selectedMunicipality}
        bind:guidedMode={guidedMode}
        bind:parcelFiles={parcelFiles}
/>
<PanelComponent
        bind:municipalities={municipalities}
        bind:stations={stations}
        bind:searchSelectedMunicipality={searchSelectedMunicipality}
        bind:selectedStation={firstSelectedStationName}
/>

<style>
    @import url("$lib/global.css");
</style>
