import React from "react";
import moment from "moment";
import { Box, Typography } from "@mui/material";
import { DATE_FORMAT, HOUR_FORMAT } from "constants";

function Spacer() {
  return <Box sx={{ height: (theme) => theme.spacing(1) }} />;
}

export default function AirfieldEphemeris({ ephemeris }) {
  const today = moment().format(DATE_FORMAT);
  const sunrise = moment(ephemeris?.sunrise).utc().format(HOUR_FORMAT);
  const daylight = moment(ephemeris?.sunrise)
    .utc()
    .subtract(30, "minutes")
    .format(HOUR_FORMAT);
  const sunset = moment(ephemeris?.sunset).utc().format(HOUR_FORMAT);
  const night = moment(ephemeris?.sunset)
    .utc()
    .add(30, "minutes")
    .format(HOUR_FORMAT);

  return (
    <Box sx={{ flexGrow: 1, mx: 1, my: { xs: 2, sm: 1 } }}>
      <Typography
        color="textSecondary"
        variant="button"
      >{`Aujourd'hui ${today}`}</Typography>
      <Spacer />
      <Typography color="textSecondary">{`Lever de soleil : ${sunrise}`}</Typography>
      <Typography
        component="span"
        color="textSecondary"
      >{`Jour aéronautique : ${daylight}`}</Typography>
      <Spacer />
      <Typography color="textSecondary">{`Coucher du soleil : ${sunset}`}</Typography>
      <Typography
        component="span"
        color="textSecondary"
      >{`Nuit aéronautique : ${night}`}</Typography>
    </Box>
  );
}
