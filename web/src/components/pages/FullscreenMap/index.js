import React from "react";
import { Box } from "@mui/material";
import OptionsMenu from "./OptionsMenu";
import Map from "./Map";

export default function FullscreenMap() {
  return (
    <Box
      sx={{
        display: "flex",
        flexGrow: 1,
        height: 0,
        position: "relative",
        overscrollBehavior: "contain",
        touchAction: "none",
      }}
    >
      <Box sx={{ flexGrow: 1 }}>
        <Map />
      </Box>
      <OptionsMenu />
    </Box>
  );
}
