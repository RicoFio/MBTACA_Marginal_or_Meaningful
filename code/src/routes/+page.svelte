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

        parcelFiles = parcelFiles.map(entry => {
            let newParcelFile = {};
            newParcelFile.StopName = entry.StopName;
            newParcelFile.FileName = entry.FileName;
            return newParcelFile;
        });
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
    $: firstSelectedStationObj = selectedStations[0];

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
        bind:selectedStationObj={firstSelectedStationObj}
        bind:selectedMunicipality={selectedMunicipality}
/>

<style>
    @import url("$lib/global.css");
</style>
