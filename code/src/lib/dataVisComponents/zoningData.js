import * as d3 from "d3";

function generateStopZoneData(data) {
    const zoningData = data[0].properties;
    const commercial = zoningData.pctZonedAsCommercial ?
        zoningData.pctZonedAsCommercial :
        zoningData.pctUsedAsCommercial;
    const multiSum = zoningData.pctUsedAsDuplex +
        zoningData.pctUsedAsTriplex +
        zoningData.pctUsedAsMultiBuildings1Lot +
        zoningData.pctUsedAsAptUpTo30Units +
        zoningData.pctUsedAsAptOver30Units +
        zoningData.pctUsedAsCoopApt +
        zoningData.pctUsedAsOtherMultifamily;
    return {
        'currentZoning': {
            other: {name: 'Other Current Zoning', value: 100 - zoningData.pctZonedAsSF - commercial - zoningData.pctZonedAsMultifamily},
            singeFamily: {name: 'Current Single Family Zoning', value: zoningData.pctZonedAsSF},
            commercial: {name: 'Current Commercial Zoning', value: commercial},
            multiFamily: {name: 'Current Multi Family Zoning', value: zoningData.pctZonedAsMultifamily}
        },
        'currentUsage': {
            other: {name: 'Other Current Usage', value: 100 - zoningData.pctUsedAsSF - commercial - zoningData.pctUsedAsCommercial - multiSum},
            singeFamily: {name: 'Current Single Family Usage', value: zoningData.pctUsedAsSF},
            commercial: {name: 'Current Commercial Usage', value: zoningData.pctUsedAsCommercial},
            multiFamily: {name: 'Current Multi Family Usage', value: multiSum}
        },
        'futureZoning': {
            other: {name: 'Other Future Zoning', value: 100 - commercial - zoningData.pctZonedAsMultifamily - zoningData.pctZonedAsSF},
            singeFamily: {name: 'Future Single Family', value: 0},
            commercial: {name: 'Future Commercial', value: commercial},
            multiFamily: {name: 'Future Multi Family', value: zoningData.pctZonedAsMultifamily + zoningData.pctZonedAsSF }
        }
    }
}

export function transformStopZoneData(originalData) {
    const zoningData = data[0].properties;
    return [
        {name: "Single Family", value: zoningData.pctZonedAsSF, category1: "pctZonedAsSF"},
        {name: "Commercial", value: zoningData.pctUsedAsCommercial, category1: "pctZonedAsComm"},
        {
            name: "Multi Family",
            value: zoningData.pctZonedAsMultifamily,
            category1: "pctZonedAsMultifamily"
        },
    ];
}
export function transformStopZoneUsageData(originalData) {
    const zoningData = data[0].properties;
    return [
        {name: "Single Family", value: zoningData.pctUsedAsSF, category1: "pctUsedAsSF"},
        {name: "Commercial", value: zoningData.pctUsedAsCommercial, category1: "pctUsedAsCommercial"},
        {
            name: "Multiple Buildings on 1 Lot",
            value: zoningData.pctUsedAsMultiBuildings1Lot,
            category1: "pctUsedAsMultiBuildings1Lot"
        },
        {name: "Duplex", value: zoningData.pctUsedAsDuplex, category1: "pctUsedAsDuplex"},
        {name: "Triplex", value: zoningData.pctUsedAsTriplex, category1: "pctUsedAsTriplex"}
    ];
}
export function transformStopZoneFutureData(originalData) {
    const zoningData = data[0].properties;
    const commercial = zoningData.pctZonedAsCommercial ?
        zoningData.pctZonedAsCommercial :
        zoningData.pctUsedAsCommercial;

    return [
        {name: "Single Family", value: 0, category1: "pctFutureZonedAsSF"},
        {name: "Commercial", value: commercial, category1: "isZonedAsCommercial"},
        {
            name: "Multi Family",
            value: zoningData.pctFutureZonedAsMulti,
            category1: "pctFutureZonedAsMulti"
        }
    ];
}

export async function loadStationZoningAndUsageData (zoningAndCensusFiles, station) {
    const fileName = zoningAndCensusFiles.filter(e => e.StopName == station.Name)[0].FileName;
    const loadedData = await d3.json(fileName);
    return generateStopZoneData(loadedData.features);
}

export async function loadStationZoningAndUsageDataDict (zoningAndCensusFiles, station) {
    const fileName = zoningAndCensusFiles.filter(e => e.StopName == station.Name)[0].FileName;
    const loadedData = await d3.json(fileName);
    return loadedData.features[0].properties
}
