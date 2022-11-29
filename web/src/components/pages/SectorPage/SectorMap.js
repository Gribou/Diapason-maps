import React from "react";
import { Stack, Box } from "@mui/material";
import LeafletLocation from "components/leaflet/LeafletLocation";
import LocationMarker from "components/leaflet/LocationMarker";
import RangeCircle from "components/leaflet/RangeCircle";
import SectorArtefact from "components/leaflet/SectorArtefact";
import useAltitudeSlider from "./AltitudeSlider";

export default function SectorMap({
  name,
  antennas,
  antennasAreAlternate,
  parts,
  zoom,
  highlightedPart,
  maxBounds,
}) {
  const slider = useAltitudeSlider({ sx: { zIndex: 500 } });
  const artefacts =
    (antennas || [])
      ?.filter((antenna) => antenna?.latitude && antenna?.longitude)
      ?.map((antenna) => [
        <LocationMarker key={2 * antenna?.pk} {...antenna} />,
        <RangeCircle
          key={2 * antenna?.pk + 1}
          {...antenna}
          altitude={slider.altitude}
          alternate={antennasAreAlternate}
        />,
      ])
      ?.flat() || [];
  const polygon = (
    <SectorArtefact
      name={name}
      parts={parts}
      key="polygon"
      highlight={highlightedPart}
    />
  );

  return (
    <Stack
      alignItems="stretch"
      justifyContent="center"
      sx={{ display: { xs: "none", sm: "flex" } }}
    >
      <Box sx={{ width: "400px", height: "300px", mt: 1 }}>
        <LeafletLocation
          artefacts={[polygon, ...artefacts]}
          zoom={zoom}
          fitBounds={maxBounds}
        />
      </Box>
      {antennas?.find((a) => a) && slider.display}
    </Stack>
  );
}
