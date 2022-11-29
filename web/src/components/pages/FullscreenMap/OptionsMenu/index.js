import React from "react";
import { Stack } from "@mui/material";
import ResetButton from "./ResetButton";
import LayersButton from "components/leaflet/pickers/LayersButton";
import ObjectsButton from "./ObjectsButton";
import AltitudeRangePicker from "./AltitudeRangePicker";

//TODO screenshot button

export default function OptionsMenu() {
  return (
    <Stack
      spacing={{ xs: 1, md: 2 }}
      alignItems="flex-end"
      sx={{ position: "absolute", top: 16, right: 16, bottom: 16, zIndex: 500 }}
    >
      <LayersButton />
      <ObjectsButton />
      <AltitudeRangePicker />
      <ResetButton />
    </Stack>
  );
}
