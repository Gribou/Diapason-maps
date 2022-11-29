import React, { useState } from "react";
import { Slider } from "@mui/material";

export const DEFAULT_SLIDER_VALUE = 50;
const MARKS = [
  { value: 0, label: "SOL" },
  { value: 100, label: "FL100" },
  { value: 200, label: "FL200" },
  { value: 300, label: "FL300" },
  { value: 400, label: "FL400" },
];

export default function useAltitudeSlider({ default_value, ...props }) {
  const [altitude, setAltitude] = useState(DEFAULT_SLIDER_VALUE);
  const [sliderValue, setSliderValue] = useState(
    default_value || DEFAULT_SLIDER_VALUE
  );
  const display = (
    <Slider
      value={sliderValue}
      min={0}
      max={400}
      step={25}
      marks={MARKS}
      color="secondary"
      valueLabelDisplay="auto"
      valueLabelFormat={(v) => `FL${v}`}
      onChange={(event, newValue) => setSliderValue(newValue)}
      onChangeCommitted={(e, newValue) => setAltitude(newValue)}
      {...props}
    />
  );

  return { altitude, display };
}
