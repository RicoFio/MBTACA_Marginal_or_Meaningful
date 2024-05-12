import * as d3 from "d3";

// "pctZonedAsSF": 0,
// "pctZonedAsCommercial": 0,
// "pctZonedAsMultifamily": 0,
// "pctUsedAsSF": 16.923842707814835,
// "pctUsedAsCommercial": 3.0363364858138375,
// "pctUsedAsDuplex": 19.16376306620209,
// "pctUsedAsTriplex": 4.579392732702837,
// "pctUsedAsMultiBuildings1Lot": 0.34843205574912894,
// "pctUsedAsAptUpTo30Units": 1.3439522150323544,
// "pctUsedAsAptOver30Units": 0,
// "pctUsedAsCoopApt": 0,
// "pctUsedAsOtherMultifamily": 0.7466401194624191,
// "pctMustUpzone": 0,
// "pctWillChange": 0,
// "pctOtherZoning": 100,
// "pctOtherUsage": 53.8576406172225

function generateStopZoneData(data) {
    const zoningData = data[0].properties;
    return {
        'currentZoning': [

        ],
        'currentUsage': [

        ],
        'futureZoning': [

        ]
    }
}

export function transformStopZoneData(originalData) {
    return [
        {name: "Single Family", value: originalData[0].properties.pctZonedAsSF, category1: "pctZonedAsSF"},
        {name: "Commercial", value: originalData[0].properties.pctUsedAsCommercial, category1: "pctZonedAsComm"},
        {
            name: "Multi Family",
            value: originalData[0].properties.pctZonedAsMultifamily,
            category1: "pctZonedAsMultifamily"
        },
    ];
}
export function transformStopZoneUsageData(originalData) {
    return [
        {name: "Single Family", value: originalData[0].properties.pctUsedAsSF, category1: "pctUsedAsSF"},
        {name: "Commercial", value: originalData[0].properties.pctUsedAsCommercial, category1: "pctUsedAsCommercial"},
        {
            name: "Multiple Buildings on 1 Lot",
            value: originalData[0].properties.pctUsedAsMultiBuildings1Lot,
            category1: "pctUsedAsMultiBuildings1Lot"
        },
        {name: "Duplex", value: originalData[0].properties.pctUsedAsDuplex, category1: "pctUsedAsDuplex"},
        {name: "Triplex", value: originalData[0].properties.pctUsedAsTriplex, category1: "pctUsedAsTriplex"}
    ];
}
export function transformStopZoneFutureData(originalData) {
    const commercial = originalData[0].properties.pctZonedAsCommercial ?
        originalData[0].properties.pctZonedAsCommercial :
        originalData[0].properties.pctUsedAsCommercial;

    return [
        {name: "Single Family", value: originalData[0].properties.pctFutureZonedAsSF, category1: "pctFutureZonedAsSF"},
        {name: "Commercial", value: commercial, category1: "isZonedAsCommercial"},
        {
            name: "Multi Family",
            value: originalData[0].properties.pctFutureZonedAsMulti,
            category1: "pctFutureZonedAsMulti"
        }
    ];
}

export async function loadStationZoningAndUsageData (zoningAndCensusFiles, station) {
    const fileName = zoningAndCensusFiles.filter(e => e.StopName == station.Name)[0].FileName;
    const loadedData = await d3.json(fileName);
    await console.log(loadedData.features);
    return {
        currentZoning: transformStopZoneData(loadedData.features),
        currentUsage: transformStopZoneUsageData(loadedData.features),
        futureZoning: transformStopZoneFutureData(loadedData.features)
    }
}
