<script>
    import { geoPath, geoCircle } from "d3-geo";
    import { line, curveNatural } from "d3";
    import { greatcircles, ports, routes } from '$lib/data/geodata.js'

    export let width;
    export let height;
    export let projection;
    export let activeLayer;

    $: path = geoPath().projection(projection);

    const lineGenerator = line().curve(curveNatural);
</script>

<svg {width} {height}>
    {#each ports.features as port}
        <circle
                cx={projection(port.geometry.coordinates)[0]}
                cy={projection(port.geometry.coordinates)[1]}
                r={5}
                fill={"#D02F35"}
                stroke={"white"}
                stroke-width={1}
        />
    {/each}
    {#if activeLayer == 'concentric'}
        {#each [250, 2000, 5000, 1000] as radius}
            <path
                    d={path(
          geoCircle()
            .center([51.28664117726216, 25.35513954451857])
            .radius((radius / (6371 * Math.PI * 2)) * 360)
            .precision(5)()
        )}
                    fill={"none"}
                    stroke={"#D02F35"}
                    stroke-width={1.5}
                    id={"path-" + radius}
            />
            <text dy={-3} fill="#D02F35">
                <textPath
                        href={"#path-" + radius}
                        startOffset={0}
                        side={"right"}>{radius + "km"}</textPath
                >
            </text>
        {/each}
    {/if}
    {#if activeLayer == 'routes'}
        {#each routes.features as route}
            <path
                    d={lineGenerator(route.geometry.coordinates.map((d) => projection(d)))}
                    fill="none"
                    stroke-width={2}
                    stroke-dasharray="4 4"
                    stroke="#D02F35"
            />
        {/each}
    {/if}

    {#if activeLayer == 'great'}
        {#each greatcircles.features as circle}
            <path
                    d={path(circle)}
                    fill="none"
                    stroke-width={1.5}
                    stroke="#D02F35"
            />
        {/each}
    {/if}
</svg>

<style>
    text {
        text-shadow: -1px -1px white, -1px 1px white, 1px 1px white, 1px -1px white, -1px 0 white, 0 1px white, 1px 0 white, 0 -1px white;
    }
</style>
