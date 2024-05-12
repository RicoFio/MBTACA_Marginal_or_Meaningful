

export function getCirclePackingColorByCategory(d) {
    switch (d.category1) {
        case "pctUsedAsCommerical":
            return "#abafa7";
        case "isZonedAsCommercial":
            return "#abafa7";
        case "pctZonedAsCommercial":
            return "#abafa7";
        case "pctZonedAsSF":
            return "#05515e";
        case "pctUsedAsSF":
            return "#05515e";
        case "pctFutureZonedAsSF":
            return "#05515e";
        case "pctFutureZonedAsMulti":
            return "#a9987a";
        case "pctZonedAsMultifamily":
            return "#999624";
        case "pctUsedAsMultiBuildings1Lot":
            return "#999624";
        case "pctUsedAsDuplex":
            return "#629681";
        case "pctUsedAsTriplex":
            return "#97340b";
        default:
            return "gray";
    }
}
