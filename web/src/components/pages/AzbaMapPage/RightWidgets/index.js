import React from "react";
import { Stack } from "@mui/material";
import LayersButton from "components/leaflet/pickers/LayersButton";

export default function RightWidgets() {
  return (
    <Stack
      spacing={{ xs: 1, md: 2 }}
      alignItems="flex-end"
      sx={{ position: "absolute", top: 70, right: 16, bottom: 16, zIndex: 500 }}
    >
      <LayersButton />
    </Stack>
  );
}
