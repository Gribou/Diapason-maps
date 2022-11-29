import React, { useState } from "react";
import { Stack, Grid, Box } from "@mui/material";
import { RadioTower } from "mdi-material-ui";
import HeaderTitle from "components/misc/HeaderTitle";
import Frequencies from "./Frequencies";
import Antennas from "./Antennas";
import VerticalBoundaries from "./VerticalBoundaries";
import SectorMap from "./SectorMap";

export default function SectorHeader({
  name,
  control_center,
  frequencies,
  main_antennas,
  alternate_antennas,
  parts,
  max_bounds,
}) {
  const [highlightedPart, setHighlightedPart] = useState();
  const [highlightedAntennas, setHighlightedAntennas] = useState();
  return (
    <Stack
      direction="row"
      sx={{
        my: { xs: 0, sm: 2 },
        ml: 2,
        maxWidth: "lg",
        position: "relative",
      }}
    >
      <Box sx={{ m: 2, ml: 0, flexGrow: 1 }}>
        <HeaderTitle title={name} subtitle={control_center} Icon={RadioTower} />
        <Grid
          container
          direction="row"
          sx={{
            maxWidth: "md",
            mt: { sm: 2 },
          }}
        >
          {frequencies && (
            <Grid item xs={12} md={6}>
              <Frequencies frequencies={frequencies} />
              {(main_antennas?.length > 0 ||
                alternate_antennas?.length > 0) && (
                <Antennas
                  main_antennas={main_antennas}
                  alternate_antennas={alternate_antennas}
                  main_selected={main_antennas === highlightedAntennas}
                  alternate_selected={
                    alternate_antennas === highlightedAntennas
                  }
                  onAntennasSelected={(antennas) =>
                    setHighlightedAntennas(antennas)
                  }
                />
              )}
            </Grid>
          )}
          {parts && (
            <Grid item xs={12} md={6}>
              <VerticalBoundaries
                parts={parts}
                selected={highlightedPart}
                onPartSelected={(pk) => setHighlightedPart(pk)}
              />
            </Grid>
          )}
        </Grid>
      </Box>
      <SectorMap
        name={name}
        antennas={highlightedAntennas}
        antennasAreAlternate={highlightedAntennas === alternate_antennas}
        parts={parts}
        highlightedPart={highlightedPart}
        maxBounds={max_bounds}
      />
    </Stack>
  );
}
