import React from "react";
import { Stack, Typography } from "@mui/material";

export default function SectorFrequencies({ frequencies }) {
  return (
    <Stack>
      <Typography color="textSecondary" variant="button" sx={{ mb: 1 }}>
        Fréquences
      </Typography>
      {frequencies?.map((freq, i) => (
        <Typography
          key={i}
          color="textSecondary"
        >{`${freq.frequency} MHz (${freq.frequency_type})`}</Typography>
      ))}
    </Stack>
  );
}
