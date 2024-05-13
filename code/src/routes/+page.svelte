<script>
    import mapboxgl from "mapbox-gl";
    import * as d3 from 'd3';
    import "../../node_modules/mapbox-gl/dist/mapbox-gl.css";
    import {onMount} from "svelte";
    import buffer from '@turf/buffer';
    import {point} from '@turf/helpers';
    import PanelComponent from '../lib/dataVisComponents/panel.svelte';
    import FloatingTooltipComponent from '../lib/tooltipComponent/FloatingTooltipComponent.svelte';
    import BaseMap from "$lib/mapComponents/BaseMap.svelte";

    mapboxgl.accessToken = "pk.eyJ1IjoicmZpb3Jpc3RhIiwiYSI6ImNsdWQwcDd0aDFkengybG85eW00eDJqdzEifQ.smRFd5P2IKrDHr5HGsfrGw";

    let baseMap;
    let stations = [];
    let parcelFiles = [];
    let zoningAndCensusFiles = [];
    let selectedMunicipality;
    let municipalities = [];
    let selectedStations = [];
    let guidedMode = true;
    let comparisonMode = false;
    let explorationMode = false;

    let resetScroll = false;
    let value = 0;

    onMount(async () => {
        let loadedStations = await d3.json("/data/mbta_community_stops.geojson");
        let loadedMunicipalities = await d3.json("/data/mbta_municipalities.geojson");
        let loadedParcelFiles = await d3.csv("/data/parcels/merged_file_name_reference.csv");
        let loadedZoningAndCensusData = await d3.csv("/data/stop_zones/file_name_reference.csv")

        stations = loadedStations.features.map(station => {
            return {
                Lat: station.geometry.coordinates[1],
                Long: station.geometry.coordinates[0],
                Community: station.properties.community,
                Name: station.properties.stop_name,
                Routes: station.properties.routes,
                RouteColors: station.properties.route_colors,
                Type: station.properties.mbta_comm_type,
                getBuffer: function (radius) {
                    return buffer(point([this.Long, this.Lat]), radius, {units: 'miles'}).geometry.coordinates[0];
                }
            };
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

        zoningAndCensusFiles = loadedZoningAndCensusData.map(entry => {
            let newParcelFile = {};
            newParcelFile.StopName = entry.StopName;
            newParcelFile.FileName = entry.FileName;
            return newParcelFile;
        });
    })

    function deselectAll(e) {
        selectedMunicipality = null;
        selectedStations = [];
        resetScroll = true;
    }
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
        bind:comparisonMode={comparisonMode}
        bind:explorationMode={explorationMode}
/>

{#key explorationMode}
    {#if !explorationMode}
        <button on:click={deselectAll} class="floating-x">
            <img src="/artwork/refresh-ccw.svg" alt="Reset and go back to the top" class="reset-icon" />
        </button>

        <div class="panel-container">
            <button on:click={deselectAll} class="floating-x">
                <img src="/artwork/refresh-ccw.svg" alt="Reset and go back to the top" class="reset-icon" />
            </button>
            <div class="progress-bar" style="position: absolute;">
                {#each [0, 1, 2, 3, 4, 5, 6, 7, 8] as slideIndex}
                    <div class="circle {value === slideIndex ? 'active' : ''}"></div>
                {/each}
            </div>
            <PanelComponent
                    bind:municipalities={municipalities}
                    bind:stations={stations}
                    bind:zoningAndCensusFiles={zoningAndCensusFiles}
                    bind:selectedMunicipality={selectedMunicipality}
                    bind:selectedStations={selectedStations}
                    bind:guidedMode={guidedMode}
                    bind:comparisonMode={comparisonMode}
                    bind:explorationMode={explorationMode}
                    bind:resetScroll={resetScroll}
                    bind:value={value}
            />
        </div>
    {:else }
        {#key selectedStations}
            {#if selectedStations.length === 2}
                <FloatingTooltipComponent
                    bind:municipality={selectedMunicipality}
                    bind:stations={selectedStations}
                    bind:zoningAndCensusFiles={zoningAndCensusFiles}
                />
            {/if}
        {/key}
    {/if}
{/key}

<style>
    @import url("$lib/global.css");

    .floating-x {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 1000;

        width: 30px;
        height: 30px;
        line-height: 30px;
        text-align: center;

        padding: 0;
        background-color: rgba(255, 255, 255, 0.8);
        border: none;
        cursor: pointer;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);

        display: flex;
        justify-content: center;
        align-items: center;
    }

    /*.panel-container {*/
    /*    display: flex;*/
    /*    width: 100%;*/
    /*}*/

    .reset-icon {
        width: 60%;  /* Adjust this to fit the button */
        height: auto; /* Keeps the aspect ratio of the image */
        transition: transform 0.3s ease; /* Smooth transition for transform */
    }

    .reset-icon:hover {
        transform: rotate(-180deg); /* Rotate 180 degrees on hover */
    }
</style>
