import React from "react";
import { Stack, Box, Grid } from "@mui/material";
import { Airport, Helicopter } from "mdi-material-ui";
import HeaderTitle from "components/misc/HeaderTitle";
import LeafletLocation from "components/leaflet/LeafletLocation";
import LocationMarker from "components/leaflet/LocationMarker";
import { AIRFIELD_ICON } from "components/leaflet/icons";
import Ephemeris from "./Ephemeris";
import Coordinates from "./Coordinates";

function AirfieldTitle({ name, category, icao_code }) {
  return (
    <HeaderTitle
      title={icao_code}
      subtitle={name}
      comment={`(${category})`}
      Icon={category?.includes("héli") ? Helicopter : Airport}
    />
  );
}

export default function AirfieldHeader({
  category,
  name,
  icao_code,
  ephemeris,
  latitude,
  longitude,
  elevation,
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
        <AirfieldTitle category={category} icao_code={icao_code} name={name} />
        <Grid
          container
          direction="row"
          sx={{
            maxWidth: "md",
            mt: { sm: 2 },
          }}
        >
          {ephemeris && (
            <Grid item xs={12} md={6}>
              <Ephemeris ephemeris={ephemeris} />
            </Grid>
          )}
          <Grid item xs={12} md={6}>
            <Coordinates
              latitude={latitude}
              longitude={longitude}
              elevation={elevation}
            />
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
                key={icao_code}
                base64icon={AIRFIELD_ICON}
                latitude={latitude}
                longitude={longitude}
              />,
            ]}
          />
        </Box>
      )}
    </Stack>
  );
}
