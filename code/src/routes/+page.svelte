<script>
    import mapboxgl from "mapbox-gl";
    import * as d3 from 'd3';
    import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    import {onMount} from "svelte";
    import buffer from '@turf/buffer';
    import { point } from '@turf/helpers';
    import PanelComponent from '../lib/dataVisComponents/panel.svelte';

    import BaseMap from "$lib/mapComponents/BaseMap.svelte";

    mapboxgl.accessToken = "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";

    let baseMap;
    let stations = [];
    let parcelFiles = [];
    let selectedMunicipality;
    let municipalities = [];
    let selectedStations = [];
    let municipalitySelected = false;
    let guidedMode = true;

    // $: console.log(parcelFiles);

    onMount(async () => {
        let loadedStations = await d3.json("/data/mbta_community_stops.geojson");
        let loadedMunicipalities = await d3.json("/data/mbta_municipalities.geojson");
        let loadedParcelFiles = await d3.csv("/data/parcels/per_station/file_name_reference.csv");

        stations = loadedStations.features.map(station => {
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

        municipalities = loadedMunicipalities.features.map(municipality => {
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

        parcelFiles = loadedParcelFiles.map(entry => {
            let newParcelFile = {};
            newParcelFile.StopName = entry.StopName;
            newParcelFile.FileName = entry.FileName;
            return newParcelFile;
        });
    })

    $: firstSelectedStation = selectedStations[0];

</script>

<BaseMap
        class="baseMap"
        bind:this={baseMap}
        bind:municipalities={municipalities}
        bind:stations={stations}
        bind:selectedStations={selectedStations}
        bind:selectedMunicipality={selectedMunicipality}
        bind:guidedMode={guidedMode}
        bind:parcelFiles={parcelFiles}
/>
<PanelComponent
        bind:municipalities={municipalities}
        bind:stations={stations}
        bind:selectedStation={firstSelectedStation}
        bind:selectedMunicipality={selectedMunicipality}
/>

<style>
    @import url("$lib/global.css");
</style>
