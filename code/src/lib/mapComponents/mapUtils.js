import mapboxgl from "mapbox-gl";

export function getCoords(longLatObj, project) {

    const longitude = parseFloat(longLatObj.Long);
    const latitude = parseFloat(longLatObj.Lat);

    if (isNaN(longitude) || isNaN(latitude)) {
        console.error("Invalid coordinates for station:", longLatObj);
        return { cx: 0, cy: 0 };
    }

    let point = new mapboxgl.LngLat(longitude, latitude);
    let {x, y} = project(point);
    return {cx: x, cy: y};
}


export function projectPolygonCoordinates(coordinates, project) {
    return coordinates.map(coord => {
        let { cx, cy } = getCoords({ Lat: coord[1], Long: coord[0] }, project);
        return `${cx},${cy}`;
    }).join(' ');
}

export function calculateBoundingBox(polygon) {
    let bounds = new mapboxgl.LngLatBounds();
    polygon.coordinates.forEach(geometry => {
        if (polygon.type.toString() == 'Polygon') {
            geometry.forEach(coord => {
                bounds.extend(coord);
            });
        } else if (polygon.type.toString() == 'MultiPolygon') {
            geometry.coordinates.forEach(subPolygon => {
                bounds.extend(subPolygon.coordinates[0])
            })
        } else {
            console.error(`Only type Polygon and MultiPolygon are supported not: ${polygon.type}`)
        }
    });
    return bounds;
}
