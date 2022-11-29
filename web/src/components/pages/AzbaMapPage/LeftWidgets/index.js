import React from "react";
import { Stack } from "@mui/material";
import ReferenceDatePickerButton from "./ReferenceDatePicker";
import ActivityOverlay from "./ActivityOverlay";

export default function LeftWidgets({ active_areas, hovered, onHover }) {
  return (
    <Stack
      spacing={{ xs: 1, md: 2 }}
      alignItems="flex-start"
      justifyContent="space-between"
      sx={{
        position: "absolute",
        left: 16,
        bottom: 16,
        top: 150,
        zIndex: 500,
      }}
    >
      <ReferenceDatePickerButton />
      <ActivityOverlay
        active_areas={active_areas}
        hovered={hovered}
        onHover={onHover}
      />
    </Stack>
  );
}
