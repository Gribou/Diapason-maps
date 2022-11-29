import React from "react";
import { useTheme } from "@mui/material";
import { Circle } from "react-leaflet";

export default function RangeCircle({
  latitude,
  longitude,
  altitude,
  highlight,
  alternate,
}) {
  const theme = useTheme();
  const altitude_m = altitude / 32.8;
  const radius = Math.sqrt((2 * 6371 + altitude_m) * altitude_m);
  const fillOpacity = highlight ? 0.4 : 0.2;
  const color = highlight
    ? theme.palette.primary.main
    : alternate
    ? theme.palette.text.secondary
    : theme.palette.secondary.light;
  return (
    <Circle
      radius={radius * 1000}
      center={[latitude?.float, longitude?.float]}
      pathOptions={{
        color,
        fillColor: color,
        fillOpacity,
      }}
    />
  );
}
