import React from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import Minimap from "./Minimap";
import "leaflet/dist/leaflet.css";

const DEFAULT_MAP_CENTER = [46, 1];
const DEFAULT_MAP_ZOOM = 4.5;

function FitBoundsControl({ bounds }) {
  const map = useMap();
  map.fitBounds(bounds, { duration: 10 });
  return null;
}

export default function Location({
  center,
  minimap,
  zoom,
  fitBounds,
  artefacts, //markers, etc
  show_osm,
  ...props
}) {
  return (
    <MapContainer
      center={center || DEFAULT_MAP_CENTER}
      zoom={zoom || DEFAULT_MAP_ZOOM}
      scrollWheelZoom={true}
      dragging
      doubleClickZoom={false}
      attributionControl={false}
      zoomControl={false}
      wheelPxPerZoomLevel={100}
      zoomSnap={0.25}
      zoomDelta={0.5}
      style={{ width: "100%", height: "100%" }}
      {...props}
    >
      {artefacts}
      {show_osm ? (
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
      ) : (
        <TileLayer
          attribution='donn&eacute;es &copy; <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>'
          url="http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
        />
      )}
      {fitBounds && <FitBoundsControl bounds={fitBounds} />}
      {minimap && <Minimap position="topright" zoom={4} />}
    </MapContainer>
  );
}
