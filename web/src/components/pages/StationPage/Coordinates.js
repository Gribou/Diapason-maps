import React from "react";
import { Box, Typography } from "@mui/material";

export default function StationCoordinates({ latitude, longitude }) {
  return (
    <Box sx={{ flexGrow: 1, mx: 1, my: { xs: 2, sm: 1 } }}>
      <Typography color="textSecondary" variant="button">
        Emplacement
      </Typography>
      <Box sx={{ height: (theme) => theme.spacing(1) }} />
      <Typography color="textSecondary">{`Latitude : ${latitude?.display}`}</Typography>
      <Typography color="textSecondary">{`Longitude : ${longitude?.display}`}</Typography>
    </Box>
  );
}
