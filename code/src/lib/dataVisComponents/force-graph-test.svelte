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
    

    let paddings = {
        top: 50
    }

    let data2 = [];
    let fig_size;

    let width = 0;
    let height = 0;

    let g;

    let filters = [
        "invert(48%) sepia(79%) saturate(2476%) hue-rotate(200deg) brightness(70%) contrast(119%)", // blue
        "invert(48%) sepia(79%) saturate(2476%) hue-rotate(80deg) brightness(70%) contrast(119%)", // green
        "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-10deg) brightness(90%) contrast(119%)", // orange
        "invert(48%) sepia(79%) saturate(2476%) hue-rotate(0deg) brightness(150%) contrast(119%)", // yellow
        "invert(48%) sepia(79%) saturate(2476%) hue-rotate(200deg) brightness(130%) contrast(80%)", // light blue
        "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-30deg) brightness(100%) contrast(119%)", // red
        "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-70deg) brightness(70%) contrast(119%)", // purple
        "invert(48%) sepia(79%) saturate(2476%) hue-rotate(80deg) brightness(130%) contrast(119%)", // light green
        "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-10deg) brightness(60%) contrast(119%)", // brown
        "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-30deg) brightness(170%) contrast(119%)", // pink
        "invert(48%) sepia(79%) saturate(3076%) hue-rotate(-220deg) brightness(100%) contrast(119%)", // teal
    ]

    let colors = [
        '#225bbc',
        '#008000',
        '#f95101',
        '#ffb300',
        '#62a9e5',
        '#ff4c47',
        '#bc2591',
        '#0ee004',
        '#f34945',
        '#ff9289',
        '#00c09b',
    ]


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
                node.x = Math.min(width - fig_size, Math.max(0, node.x));
                node.y = Math.min(height - fig_size, Math.max(node.y, paddings.top));
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
                        fill='#000000'
                    >{d.label}</text>
                {/each}
            {/if}
        </g>
        <g bind:this={g}/>
    </VisualizationWrapper>
    {#if mousePosition.x != null && currentHoveredPoint}
        <div
            class={mousePosition.x === null ? "tooltip-hidden" : "tooltip-visible"}
            style="left: {pageMousePosition.x + 10}px; top: {pageMousePosition.y + 10}px"
        >
            About {currentHoveredPoint.value.toFixed(2)}% of migrants experience violence as a result of {currentHoveredPoint.label}
        </div>
    {/if}
</div>

<style>
    .icon:hover {
        padding: 2vh;
        background-color: aqua;
    }

    .tooltip-hidden {
        visibility: hidden;
        font-family: "Nunito", sans-serif;
        width: 200px;
        position: absolute;
    }

    .tooltip-visible {
        font: 18px sans-serif;
        font-family: "Nunito", sans-serif;
        visibility: visible;
        background-color: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(8px);
        border-radius: 10px;
        width: 200px;
        color: black;
        position: absolute;
        padding: 10px;
    }

</style>