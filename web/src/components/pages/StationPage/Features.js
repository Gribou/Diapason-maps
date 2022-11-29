import React from "react";
import { Box, Typography } from "@mui/material";

export default function StationFeatures({ frequency, range }) {
  return (
    <Box sx={{ flexGrow: 1, mx: 1, my: { xs: 2, sm: 1 } }}>
      <Typography color="textSecondary" variant="button">
        Caractéristiques
      </Typography>
      <Box sx={{ height: (theme) => theme.spacing(1) }} />
      <Typography color="textSecondary">{`Fréquence : ${frequency}`}</Typography>
      <Typography color="textSecondary">{`Portée : ${range}`}</Typography>
    </Box>
  );
}
