import React, { useState } from "react";
import { Stack, Typography, IconButton } from "@mui/material";
import { Eye, EyeOff } from "mdi-material-ui";
import { useTouchOnly } from "features/ui";

export default function SectorVerticalBoundaries({
  parts,
  onPartSelected,
  selected,
}) {
  const [showButton, setShowButton] = useState();
  const touchOnly = useTouchOnly();
  return (
    <Stack sx={{ mt: { xs: 3, md: 0 } }}>
      <Typography color="textSecondary" variant="button" sx={{ mb: 1 }}>
        Limites verticales
      </Typography>
      {parts
        ?.map(({ ceiling, floor, pk }) => (
          <Stack
            direction="row"
            alignItems="center"
            key={pk}
            onMouseOver={() => setShowButton(pk)}
            onMouseOut={() => setShowButton()}
            onClick={() =>
              selected === pk ? onPartSelected() : onPartSelected(pk)
            }
            sx={{ position: "relative" }}
          >
            <IconButton
              size="small"
              sx={{
                p: 0,
                opacity: touchOnly || showButton === pk ? 1 : 0,
                position: "absolute",
                left: "-32px",
              }}
            >
              {selected === pk ? <EyeOff /> : <Eye />}
            </IconButton>
            <Typography
              color="textSecondary"
              sx={{
                cursor: "pointer",
                fontWeight: selected === pk ? "bold" : undefined,
              }}
            >{`${floor} - ${ceiling}`}</Typography>
          </Stack>
        ))
        ?.reverse()}
    </Stack>
  );
}
