import React from "react";
import { MapContainer } from "react-leaflet";
import Minimap from "components/leaflet/Minimap";
import { useSearchParams } from "features/router";
import { useInfo } from "features/info/hooks";

import Layers from "components/leaflet/by_search_params/Layers";
import MapCallback from "components/leaflet/by_search_params/MapCallback";
import Antennas from "./Antennas";
import Airfields from "./Airfields";
import Sectors from "./Sectors";
import Stations from "./Stations";
import KMLMaps from "./KMLMaps";
import "leaflet/dist/leaflet.css";

const DEFAULT_MAP_CENTER = [46.8, 3];
const DEFAULT_MAP_ZOOM = 6.5;

export default function Map({ minimap, ...props }) {
  const { radio_coverage_enabled } = useInfo();
  const [{ zoom, center_lat, center_lon }] = useSearchParams();
  const center =
    center_lat && center_lon ? [center_lat, center_lon] : DEFAULT_MAP_CENTER;

  return (
    <MapContainer
      preferCanvas={true}
      center={center}
      zoom={zoom || DEFAULT_MAP_ZOOM}
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
      style={{ width: "100%", height: "100%" }}
      {...props}
    >
      <KMLMaps />
      <Airfields />
      <Sectors />
      <Stations />
      {radio_coverage_enabled && <Antennas />}
      <Layers />
      {minimap && <Minimap position="topright" zoom={4} />}
      <MapCallback />
    </MapContainer>
  );
}
