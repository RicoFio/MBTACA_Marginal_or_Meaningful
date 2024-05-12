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