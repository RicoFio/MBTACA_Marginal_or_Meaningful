

export function getCirclePackingColorByCategory(d) {
    console.log(d.category1);
    switch (d.category1) {
        case "pctUsedAsComm":
            return "#97340b";
        case "pctUsedAsCommerical":
            return "#97340b";
        case "pctUsedAsCommercial":
            return "#97340b";
        case "isZonedAsCommercial":
            return "#97340b";
        case "pctZonedAsCommercial":
            return "#97340b";
        case "pctZonedAsSF":
            return "#f39034";
        case "pctUsedAsSF":
            return "#f39034";
        case "pctFutureZonedAsSF":
            return "#f39034";
        case "pctFutureZonedAsMulti":
            return "#999624";
        case "pctZonedAsMultifamily":
            return "#999624";
        case "pctUsedAsMultiBuildings1Lot":
            return "#999624";
        case "pctUsedAsDuplex":
            return "#999624";
        case "pctUsedAsTriplex":
            return "#999624";
        default:
            return "#abafa7";
    }
}
