import React, { useState, useEffect, Fragment } from "react";
import { Slider, Typography } from "@mui/material";
import { from_timestamp, now } from "./utils";

export default function TimestampSlider({ defaultValue, min, max, onSubmit }) {
  const [pending, setPending] = useState(defaultValue);

  //next 24 hours or max
  const max_date = Math.min(now() + 3600 * 24, max) || now() + 3600 * 24;
  // last 24 hours or min
  const min_date = Math.max(now() - 3600 * 24, min) || now() - 3600 * 24;

  useEffect(() => {
    setPending(defaultValue);
  }, [defaultValue]);

  return (
    <Fragment>
      <Typography
        variant="caption"
        sx={{
          wordWrap: "break-word",
          mr: 2,
        }}
        align="center"
      >
        {from_timestamp(min_date)}
      </Typography>
      <Slider
        color="secondary"
        value={pending}
        step={3600} //1 step per hour
        min={min_date}
        max={max_date}
        onChange={(event, newValue) => setPending(newValue)}
        onChangeCommitted={(event, newValue) => onSubmit(newValue)}
        valueLabelDisplay="on"
        valueLabelFormat={() => `${from_timestamp(pending)} TU`}
      />
      <Typography
        variant="caption"
        sx={{
          wordWrap: "break-word",
          ml: 2,
        }}
      >
        {from_timestamp(max_date)}
      </Typography>
    </Fragment>
  );
}
