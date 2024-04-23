<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    export let data = [];

    let data = [
        { name: "A", value: 10 },
        { name: "B", value: 20 },
        { name: "C", value: 30 },
        { name: "D", value: 40 },
    ];

    onMount(() => {
        drawTreemap();
    });

    function drawTreemap() {
        const width = 600;
        const height = 400;

        const svg = d3
            .select("svg")
            .attr("width", width)
            .attr("height", height);

        const root = d3.hierarchy({ children: data }).sum((d) => d.value);

        const treemap = d3.treemap().size([width, height]).padding(1);

        treemap(root);

        const cell = svg
            .selectAll("g")
            .data(root.leaves())
            .enter()
            .append("g")
            .attr("transform", (d) => `translate(${d.x0},${d.y0})`);

        cell.append("rect")
            .attr("width", (d) => d.x1 - d.x0)
            .attr("height", (d) => d.y1 - d.y0)
            .attr("fill", "steelblue")
            .on("mouseover", handleMouseOver)
            .on("mouseout", handleMouseOut);

        cell.append("text")
            .attr("x", 5)
            .attr("y", 15)
            .text((d) => d.data.name)
            .attr("fill", "white");

        function handleMouseOver() {
            d3.select(this).attr("fill", "orange");
        }

        function handleMouseOut() {
            d3.select(this).attr("fill", "steelblue");
        }
    }
</script>

<svg></svg>
