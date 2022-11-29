import React, { useState, useRef } from "react";
import { Fab, Tooltip, Stack, Paper, Slide, Grow } from "@mui/material";
import { ClockOutline } from "mdi-material-ui";

import { useReferenceDates } from "./utils";
import DateTimePickerButton from "./DateTimePickerButton";
import ResetToNowButton from "./ResetToNowButton";
import TimestampSlider from "./TimestampSlider";

export default function ReferenceDatePickerButton() {
  const buttonRef = useRef(null);
  const [show, setShow] = useState(false);
  const { current, min, max, set } = useReferenceDates();

  return !min ? null : (
    <Stack
      direction="row"
      alignItems="stretch"
      sx={{ flex: "0 0 48px" }}
      spacing={4}
    >
      <Tooltip title="Date & Heure" placement="left">
        <Fab size="medium" onClick={() => setShow(!show)} ref={buttonRef}>
          <ClockOutline />
        </Fab>
      </Tooltip>
      <Slide direction="right" in={show} container={buttonRef.current}>
        <Grow in={show}>
          <Stack
            direction="row"
            alignItems="center"
            component={Paper}
            elevation={6}
            sx={{
              zIndex: 1050,
              borderRadius: "24px",
              width: "360px",
              height: "48px",
              backgroundColor: "#e0e0e0",
              "&:hover": {
                backgroundColor: "#fff",
              },
              px: 1,
            }}
          >
            <TimestampSlider
              defaultValue={current}
              onSubmit={set}
              min={min}
              max={max}
            />
            <DateTimePickerButton
              defaultValue={current}
              onSubmit={set}
              min={min}
              max={max}
            />
            <ResetToNowButton onSubmit={set} />
          </Stack>
        </Grow>
      </Slide>
    </Stack>
  );
}
