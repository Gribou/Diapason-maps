import React from "react";
import { Stack, Typography, Checkbox } from "@mui/material";

export default function LayerTreeItemContent({ label, selected }) {
  return (
    <Stack direction="row" alignItems="center" spacing={1}>
      <Checkbox
        edge="start"
        checked={selected || false}
        tabIndex={-1}
        disableRipple
        color="secondary"
        sx={{ p: 1 }}
      />
      <Typography noWrap>{label}</Typography>
    </Stack>
  );
}

//display depth as well ?
