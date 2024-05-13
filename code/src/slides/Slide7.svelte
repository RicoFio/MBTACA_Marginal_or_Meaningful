<script>

    export let active = false;

    export let guidedMode, comparisonMode, explorationMode;

    function handleExploreButton(e) {
        guidedMode = false;
        comparisonMode = false;
        explorationMode = true;
    }
</script>

<div class="slide">
    <h1>WHAT DOES THIS TELL US?</h1>
    <p>
        The main takeaway from this analysis is that the
        impacts of siting a by-right multifamily district vary significantly between municipalities and stations
        within the same municipality.
        <br>
        We can also see that the population living near Rapid Transit stops are
        much more likely to take transit to work than those living near the commuter tail. This has implications
        for the MBTA Communities Act because it speaks to the differences in behavioral patterns of residents
        living near different communities.
        <br>
        <br>
        And how is the situation in other municipalities or for other stations?
    </p>

    <button class="explore-button" on:click={handleExploreButton}>
        EXPLORE NOW
    </button>

    <br>
    <br>
    <h2>Data sources and Acknowledgments</h2>
    <p>
        This project was developed with guidance and feedback from the <a href="https://www.mapc.org/" target="_blank">Metropolitan
        Area Planning Commission (MAPC)</a>.
        Shapefiles for the MBTA communities come from the 2020 census, retrieved from Social Explorer.
        Demographic data is sourced from the 2022 ACS 5-year rolling estimates (downloaded from Social Explorer).
        Stop zones were created from the parcel data shapefiles downloaded from mass GIS and interpreted with
        usage code designations for the state of Massachusetts from <a href="https://cityofboston.gov" target="_blank">CityOfBoston.gov</a>
        and the Zoning Atlas created by the MAPC.
        Additional background information was retrieved from
        <a href=https://www.wbur.org/radioboston/2023/11/27/mbta-communites-act-density-transit-oriented-housing
           target="_blank">www.wbur.org</a> and
        <a href=https://www.mass.gov/info-details/multi-family-zoning-requirement-for-mbta-communities target="_blank">www.mass.gov</a>.
    </p>
</div>

<style>
    @import url("$lib/slide.css");

    .explore-button {
        background-color: white; /* White background */
        color: black; /* Text color */
        border: none; /* No border */
        padding: 10px 20px; /* Padding around the text */
        font-size: 16px; /* Text size */
        font-weight: bold; /* Font weight */
        border-radius: 25px; /* Rounded corners */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Shadow for 3D effect */
        transition: all 0.3s; /* Smooth transition for mouse events */
        cursor: pointer; /* Pointer cursor on hover */
        outline: none; /* Remove outline on focus */
    }

    .explore-button:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Enhanced shadow on hover */
        transform: translateY(-2px); /* Slight raise on hover */
    }

    .explore-button:active {
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Smaller shadow on click */
        transform: translateY(1px); /* Slight press down on click */
    }

    .slide a { /* Targeting all anchor tags within elements with class 'slide' */
        color: white; /* Sets the text color to white */
        text-decoration: none; /* Optional: Removes underline from links */
    }

    .slide a:hover { /* Styling for hover state of the links */
        text-decoration: underline; /* Optional: Adds underline on hover */
    }
</style>