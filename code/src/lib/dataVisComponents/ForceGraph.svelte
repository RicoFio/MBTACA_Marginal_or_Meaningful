<script>
    import * as d3 from "d3";
    import VisualizationWrapper from "./VisualizationWrapper.svelte";
    import { onMount } from "svelte";

    export let cssHeight;
    export let cssWidth;
    export let data;
    export let Title = "";
    export let fcenter = 1.0;
    export let fcharge = 0.5;
    export let fcollide = 0.6;
    export let flink = 0.3;
    export let legend=true;
    export let selectedCategory;

    let legendWidth = 170;
    let legendMargin = 50;
    

    let paddings = {
        top: 50
    }

    let data2 = [];
    let fig_size;

    let width = 0;
    let height = 0;

    let g;

    let filters = [
        "saturate(100%) invert(24%) sepia(10%) saturate(7275%) hue-rotate(153deg) brightness(93%) contrast(96%)", // #05515e
        "saturate(100%) invert(37%) sepia(7%) saturate(3561%) hue-rotate(42deg) brightness(80%) contrast(99%)", // #3e5719
        "saturate(100%) invert(91%) sepia(2%) saturate(4416%) hue-rotate(349deg) brightness(67%) contrast(97%)", // #a9987a
        "saturate(100%) invert(22%) sepia(85%) saturate(1384%) hue-rotate(353deg) brightness(92%) contrast(99%)", // #97340b
        "saturate(100%) invert(58%) sepia(15%) saturate(776%) hue-rotate(104deg) brightness(91%) contrast(81%)", // #629681
        "saturate(100%) invert(87%) sepia(12%) saturate(130%) hue-rotate(47deg) brightness(80%) contrast(84%)", // #abafa7
        "saturate(100%) invert(59%) sepia(53%) saturate(576%) hue-rotate(331deg) brightness(92%) contrast(88%)", // #dd8155
        "saturate(100%) invert(79%) sepia(28%) saturate(6443%) hue-rotate(338deg) brightness(100%) contrast(91%)", // #f39034
        "saturate(100%) invert(64%) sepia(1%) saturate(2277%) hue-rotate(314deg) brightness(93%) contrast(84%)", // #9f9090
        "saturate(100%) invert(56%) sepia(38%) saturate(695%) hue-rotate(20deg) brightness(92%) contrast(99%)", // #999624
        // "invert(48%) sepia(79%) saturate(2476%) hue-rotate(200deg) brightness(70%) contrast(119%)", // blue
        // "invert(48%) sepia(79%) saturate(2476%) hue-rotate(80deg) brightness(70%) contrast(119%)", // green
        // "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-10deg) brightness(90%) contrast(119%)", // orange
        // "invert(48%) sepia(79%) saturate(2476%) hue-rotate(0deg) brightness(150%) contrast(119%)", // yellow
        // "invert(48%) sepia(79%) saturate(2476%) hue-rotate(200deg) brightness(130%) contrast(80%)", // light blue
        // "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-30deg) brightness(100%) contrast(119%)", // red
        // "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-70deg) brightness(70%) contrast(119%)", // purple
        // "invert(48%) sepia(79%) saturate(2476%) hue-rotate(80deg) brightness(130%) contrast(119%)", // light green
        // "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-10deg) brightness(60%) contrast(119%)", // brown
        // "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-30deg) brightness(170%) contrast(119%)", // pink
        // "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-220deg) brightness(100%) contrast(119%)", // teal
    ]

    let colors = [
        '#05515e',
        '#3e5719',
        '#a9987a',
        '#97340b',
        '#629681',
        '#abafa7',
        '#dd8155',
        '#f39034',
        '#9f9090',
        '#999624',
    ];


    onMount(() => {
        data2 = data.map((d,i) => [...Array(Math.floor(d.value)).keys()].map(e => {
            return {
                id: `${i}-${e}`,
                category: i,
                index: e,
                protagonist: d.includes_protagonist && e == 0,
                dark: e >= d.highlighted 
            }
        })).flat()

        let links = data.map((d,i) => [...Array(Math.floor(d.value)).keys()].map(e => {
            return {source:`${i}-0`, target:`${i}-${e}`}
        })).flat()

        fig_size = Math.min(width, height)/18

        var node = d3.select(g)
            .selectAll("image")
            .data(data2)
            .enter()
            .append("image")
                .attr("class", "node")
                .attr("xlink:href", "images/human_icon.png")
                .attr("x", (d) => (width / 2))
                .attr("y", d => (height / 2))
                .attr("height", fig_size)
                .attr("onmouseover", `this.style.opacity=0.7`)
                .attr("onmouseout", d => `this.style.opacity=${d.dark ? 0.3 : 1}`)
                .style("filter", d => d.protagonist ? filters[6] : filters[d.category])
                .style("opacity", d => d.dark ? 0.3 : 1.0)


        var simulation = d3.forceSimulation(data2)
            .force("center", d3.forceCenter().strength(fcenter).x(width/2).y(height/2))
            .force("charge", d3.forceManyBody().strength(fcharge))
            .force("collide", d3.forceCollide().strength(fcollide).radius(fig_size/2).iterations(1))
            .force("link", d3.forceLink().strength(flink).id(d => d.id))
            .force("bound", () => {data2.forEach(node => {
                node.x = Math.min(width - fig_size - legendWidth - legendMargin, Math.max(0, node.x));
                node.y = Math.min(height - fig_size - legendMargin, Math.max(node.y, paddings.top));
            })})

        simulation
            .nodes(data2)
            .on("tick", (d) => {
                node
                    .attr("x", d => d.x)
                    .attr("y", d => d.y)
            })
            .force("link").links(links)

    })

    const idContainer = "svg-container-" + Math.random() * 1000000;
    let mousePosition = { x: null, y: null };
    let pageMousePosition = { x: null, y: null };
    let currentHoveredPoint = null;

    function followMouse(event) {
        const svg = document.getElementById(idContainer);
        if (svg === null) return;
        const dim = svg.getBoundingClientRect();
        pageMousePosition = {
            x: event.pageX,
            y: event.pageY,
        };
        const positionInSVG = {
            x: event.clientX - dim.left,
            y: event.clientY - dim.top,
        };
        mousePosition = { x: positionInSVG.x, y: positionInSVG.y }
        computeSelectedValue(mousePosition)
    }
    function removePointer() {
        mousePosition = { x: null, y: null };
        currentHoveredPoint = null;
    }

    function computeSelectedValue(mousePosition) {

        for (let point of data2) {
            let dis = Math.sqrt((mousePosition.x - point.x) ** 2 + (mousePosition.y - point.y) ** 2)
            if (dis < (fig_size/2)) {
                currentHoveredPoint = data[point.category]
                break;
            }
        }
    }


</script>

<div>
    <VisualizationWrapper
        cssHeight={cssHeight}
        cssWidth={cssWidth}
        mousemove={followMouse}
        mouseleave={removePointer}
        bind:chartWidth={width}
        bind:chartHeight={height}
        id={idContainer}
    >
        <g>
            <text
                x={width/2}
                y={paddings.top/2}
                font-size="24"
                fill="#000000"
            >
                {Title}
            </text>
        </g>
        <g>
            {#if data2.length > 0 && legend}
                {#each data as d, index}
                    <rect
                        x={width-169}
                        y={20 * (index - data.length/2)+ height/2}
                        height={10}
                        width={10}
                        fill={colors[index]}
                    />
                    <text
                        x={width-154}
                        y={20 * (index - data.length/2) + 10 + height/2}
                        fill='#a9987a'
                    >{d.label}</text>
                {/each}
            {/if}
        </g>
        <g bind:this={g}/>
    </VisualizationWrapper>
    {#if mousePosition.x != null && currentHoveredPoint}
        <div
            class={mousePosition.x === null ? "tooltip-forcegraph-hidden" : "tooltip-forcegraph-visible"}
            style="left: {pageMousePosition.x + 10}px; top: {pageMousePosition.y + 10}px"
        >

        {#if selectedCategory == "age"}
            About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area are of age {currentHoveredPoint.label}.
        {:else if selectedCategory == "race"}
            {#if currentHoveredPoint.value == 'other_race'}
                About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area belong to another race.
            {:else}
                About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area are {currentHoveredPoint.label}.
            {/if}
        {:else if selectedCategory == "gender"}
            About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area are {currentHoveredPoint.label}.
        {:else if selectedCategory == "median household income"}
            {#if currentHoveredPoint.value == 5}
            The top 5% of households in the selected area have a median income of {currentHoveredPoint.label}.
            {:else}
            About {currentHoveredPoint.value.toFixed(2)}% of households in the selected area have a median income of {currentHoveredPoint.label}.
            {/if}
        {:else if selectedCategory == "vehicles per household"}
            {#if currentHoveredPoint.label == 'one'}
            About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area own {currentHoveredPoint.label} vehicle.
            {:else}
            About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area own {currentHoveredPoint.label} vehicles.
            {/if}
        {:else if selectedCategory == "mode of transportation"}
            {#if currentHoveredPoint.label == "work_from_home"}
            About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area work from home.
            {:else if currentHoveredPoint.label == "public_transport"}
            About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area commute to work by public transport.
            {:else}
            About {currentHoveredPoint.value.toFixed(2)}% of inhabitants in the selected area commute to work by {currentHoveredPoint.label}.
            {/if}
        {/if}
            <!-- About {currentHoveredPoint.value.toFixed(2)}% of migrants experience violence as a result of {currentHoveredPoint.label} -->
        </div>
    {/if}
</div>

<style>
    .icon:hover {
        padding: 2vh;
        background-color: #000000;
    }

    .tooltip-forcegraph-hidden {
        visibility: hidden;
        font-family: 'Montserrat', sans-serif;
        width: 200px;
        position: absolute;
    }

    .tooltip-forcegraph-visible {
        z-index: 100;
        font: 18px sans-serif;
        font-family: 'Montserrat', sans-serif;
        visibility: visible;
        background-color: rgba(10, 0, 0, 0.4);
        backdrop-filter: blur(8px);
        border-radius: 10px;
        width: 200px;
        color: #a9987a;
        position: fixed;
        padding: 10px;
    }
</style>