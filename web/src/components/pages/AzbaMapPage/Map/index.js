import React from "react";
import { MapContainer } from "react-leaflet";
import Layers from "components/leaflet/by_search_params/Layers";
import MapCallback from "components/leaflet/by_search_params/MapCallback";
import AzbaArtefact from "./AzbaArtefact";
import "leaflet/dist/leaflet.css";

export default function Map({ active_areas, hovered, onHover }) {
  return (
    <MapContainer
      preferCanvas={true}
      center={[46.8, 3]}
      zoom={6.5}
      // bounds={[
      //   [51, -5],
      //   [40, 9],
      // ]}
      // boundsOptions={{padding: [50, 50]}}
      scrollWheelZoom
      dragging
      doubleClickZoom={false}
      attributionControl={false}
      tap={false} //corrects bug with Popup on iOS/ipadOS. Leaflet v1.7.1
      zoomControl
      zoomSnap={0.25}
      zoomDelta={0.5}
      wheelPxPerZoomLevel={100}
      style={{
        width: "100%",
        height: "100%",
        outline: "none",
      }}
    >
      {active_areas?.map(({ slug, ...area }) => (
        <AzbaArtefact
          key={slug}
          {...area}
          slug={slug}
          hovered={hovered === slug}
          onHover={onHover}
        />
      ))}
      <Layers />
      <MapCallback />
    </MapContainer>
  );
}
