import React, { useState } from "react";
import { Stack, Typography, IconButton } from "@mui/material";
import { Eye, EyeOff } from "mdi-material-ui";
import { useTouchOnly } from "features/ui";

function AntennaDisplay({ label, antennas, onAntennasSelected, selected }) {
  const [showButton, setShowButton] = useState(false);
  const touchOnly = useTouchOnly();
  return (
    <Stack
      direction="row"
      alignItems="center"
      onMouseOver={() => setShowButton(true)}
      onMouseOut={() => setShowButton(false)}
      onClick={() =>
        selected ? onAntennasSelected() : onAntennasSelected(antennas)
      }
      sx={{ position: "relative" }}
    >
      <IconButton
        size="small"
        sx={{
          p: 0,
          opacity: touchOnly || showButton ? 1 : 0,
          position: "absolute",
          left: "-32px",
        }}
      >
        {selected ? <EyeOff /> : <Eye />}
      </IconButton>
      <Typography
        color="textSecondary"
        sx={{
          cursor: "pointer",
          fontWeight: selected ? "bold" : undefined,
        }}
      >
        {`${label} : ${antennas?.map((a) => a.name)?.join(" + ")}`}
      </Typography>
    </Stack>
  );
}

export default function SectorAntennas({
  main_antennas,
  alternate_antennas,
  main_selected,
  alternate_selected,
  onAntennasSelected,
}) {
  return (
    <Stack sx={{ mt: 3 }}>
      <Typography color="textSecondary" variant="button" sx={{ mb: 1 }}>
        Antennes
      </Typography>
      {main_antennas?.length > 0 && (
        <AntennaDisplay
          label={`Antenne${main_antennas?.length > 1 ? "s" : ""} principale${
            main_antennas?.length > 1 ? "s" : ""
          }`}
          antennas={main_antennas}
          onAntennasSelected={onAntennasSelected}
          selected={main_selected}
        />
      )}
      {alternate_antennas?.length > 0 && (
        <AntennaDisplay
          label={`Antenne${alternate_antennas?.length > 1 ? "s" : ""} secours`}
          antennas={alternate_antennas}
          selected={alternate_selected}
          onAntennasSelected={onAntennasSelected}
        />
      )}
    </Stack>
  );
}
