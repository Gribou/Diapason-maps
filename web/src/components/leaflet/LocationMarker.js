import React from "react";
import { Marker, Tooltip } from "react-leaflet";
import { ANTENNA_ICON } from "components/leaflet/icons";
import L from "leaflet";

export default function LocationMarker({
  latitude,
  longitude,
  name,
  highlight,
  base64icon = ANTENNA_ICON,
  children,
  ...props
}) {
  const icon = new L.Icon({
    iconUrl: `data:image/svg+xml;base64,${base64icon}`,
    iconSize: [32, 48],
    iconAnchor: [10, 15],
  });

  return (
    <Marker
      icon={icon}
      position={[latitude?.float, longitude?.float]}
      {...props}
    >
      {/*force re-render of tooltip because permanent is not mutable*/}(
      {children ||
        (name && (
          <Tooltip permanent={highlight} key={`${name}-${highlight}`}>
            {name}
          </Tooltip>
        ))}
    </Marker>
  );
}
