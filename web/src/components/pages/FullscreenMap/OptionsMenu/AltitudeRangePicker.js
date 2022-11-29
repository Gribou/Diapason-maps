import React, { useState } from "react";
import { Paper, Slider, Typography, Stack } from "@mui/material";
import { useSearchParams } from "features/router";

export const DEFAULT_SLIDER_VALUE = [0, 400];
const MARKS = [
  { value: 0, label: "SOL" },
  { value: 100, label: "100" },
  { value: 200, label: "200" },
  { value: 300, label: "300" },
  { value: 400, label: "400" },
];

export default function AltitudeRangePicker() {
  const [{ ceiling, floor, ...params }, push] = useSearchParams();
  const [sliderValue, setSliderValue] = useState([
    parseInt(floor, 10) || DEFAULT_SLIDER_VALUE[0],
    parseInt(ceiling, 10) || DEFAULT_SLIDER_VALUE[1],
  ]);

  function preventHorizontalKeyboardNavigation(event) {
    // for webkit compatibility
    //https://mui.com/material-ui/react-slider/#vertical-sliders
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
    }
  }

  const onSubmit = (e, newValue) => {
    push({
      ...params,
      floor: `${Math.min(...newValue)}`,
      ceiling: `${Math.max(...newValue)}`,
    });
  };

  return (
    <Stack
      component={Paper}
      elevation={6}
      sx={{
        zIndex: 1050,
        borderRadius: "24px",
        minHeight: "120px",
        maxHeight: "480px",
        flexGrow: 1,
        width: "48px",
        py: { xs: 0, md: "8px" },
        backgroundColor: "#e0e0e0",
        "&:hover": {
          backgroundColor: "#fff",
        },
      }}
      alignItems="center"
      spacing={{ xs: 0, sm: 2 }}
    >
      <Slider
        orientation="vertical"
        color="secondary"
        min={0}
        max={400}
        step={10}
        marks={MARKS}
        value={sliderValue}
        onKeyDown={preventHorizontalKeyboardNavigation}
        onChange={(event, newValue) => setSliderValue(newValue)}
        onChangeCommitted={onSubmit}
        valueLabelDisplay="auto"
        valueLabelFormat={(v) => `FL${v}`}
        sx={{
          '& input[type="range"]': {
            WebkitAppearance: "slider-vertical",
          },
          m: 0,
          mt: "20px",
          ml: "26px",
          p: 0,
          "@media (pointer: coarse)": {
            p: 0,
          },
          "& .MuiSlider-thumb": {
            width: "18px",
            height: "18px",
          },
          "& .MuiSlider-markLabel": {
            left: "-30px",
            fontSize: 12,
          },
          "& .MuiSlider-valueLabel": {
            "&:before": {
              right: "-15%",
            },
          },
        }}
      />
      <Typography variant="button">FL</Typography>
    </Stack>
  );
}
