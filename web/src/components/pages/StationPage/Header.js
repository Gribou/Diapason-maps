import React from "react";
import { Stack, Box, Grid } from "@mui/material";
import { RadioTower } from "mdi-material-ui";

import HeaderTitle from "components/misc/HeaderTitle";
import LeafletLocation from "components/leaflet/LeafletLocation";
import LocationMarker from "components/leaflet/LocationMarker";
import { RADIO_TOWER_ICON } from "components/leaflet/icons";
import Coordinates from "./Coordinates";
import Features from "./Features";

function StationTitle({ short_name, long_name, types }) {
  return (
    <HeaderTitle
      title={short_name}
      subtitle={long_name}
      comment={`(${[...types].reverse().join("-")})`}
      Icon={RadioTower}
    />
  );
}

export default function Header({
  short_name,
  long_name,
  latitude,
  longitude,
  frequency,
  range,
  types,
}) {
  return (
    <Stack
      direction="row"
      sx={{
        my: { xs: 0, sm: 2 },
        maxWidth: "lg",
      }}
    >
      <Box sx={{ m: 2, ml: 0, flexGrow: 1 }}>
        <StationTitle
          short_name={short_name}
          long_name={long_name}
          types={types}
        />
        <Grid
          container
          direction="row"
          sx={{
            maxWidth: "md",
            mt: { sm: 2 },
          }}
        >
          <Grid item xs={12} md={6}>
            <Features frequency={frequency} range={range} />
          </Grid>
          <Grid item xs={12} md={6}>
            <Coordinates latitude={latitude} longitude={longitude} />
          </Grid>
        </Grid>
      </Box>

      {latitude && longitude && (
        <Box
          sx={{
            display: { xs: "none", sm: "block" },
            width: { sm: "200px", md: "400px" },
            height: { sm: "200px", md: "300px" },
          }}
        >
          <LeafletLocation
            center={[latitude?.float, longitude?.float]}
            zoom={13}
            minimap
            show_osm
            artefacts={[
              <LocationMarker
                key={short_name}
                latitude={latitude}
                longitude={longitude}
                base64icon={RADIO_TOWER_ICON}
              />,
            ]}
          />
        </Box>
      )}
    </Stack>
  );
}
