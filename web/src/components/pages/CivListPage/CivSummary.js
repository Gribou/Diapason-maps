import React from "react";
import moment from "moment";
import { Stack, Typography, Box } from "@mui/material";
import { WeatherSunny, WeatherNight } from "mdi-material-ui";
import HeaderTitle from "components/misc/HeaderTitle";

const TU_HOUR_FORMAT = "HH:mm TU";
const HOUR_FORMAT = "HH:mm";
const DATE_FORMAT = "DD/MM/YYYY";

function Spacer() {
  return <Box sx={{ height: (theme) => theme.spacing(1) }} />;
}

export default function CivSummary({
  label,
  is_open,
  open_at,
  closed_at,
  sunset,
  sunrise,
}) {
  const today = moment().format(DATE_FORMAT);
  return (
    <Stack alignItems="center">
      <HeaderTitle title={label} Icon={is_open ? WeatherSunny : WeatherNight} />
      <Typography
        color="textSecondary"
        variant="button"
        sx={{ mt: 2 }}
      >{`Aujourd'hui ${today}`}</Typography>
      <Spacer />
      <Typography component="span" color="textSecondary">{`Ouverture : ${moment(
        open_at
      ).format(HOUR_FORMAT)} (${moment(open_at)
        .utc()
        .format(TU_HOUR_FORMAT)})`}</Typography>
      <Typography component="span" color="textSecondary">
        {`Fermeture : ${moment(closed_at).format(HOUR_FORMAT)} (${moment(
          closed_at
        )
          .utc()
          .format(TU_HOUR_FORMAT)})`}
      </Typography>
      {(sunrise || sunset) && <Spacer />}
      {sunrise && (
        <Typography color="textSecondary">
          {`Lever du soleil : ${moment(sunrise).utc().format(TU_HOUR_FORMAT)}`}
        </Typography>
      )}
      {sunset && (
        <Typography color="textSecondary">{`Coucher du soleil : ${moment(sunset)
          .utc()
          .format(TU_HOUR_FORMAT)}`}</Typography>
      )}
    </Stack>
  );
}
