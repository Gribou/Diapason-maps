import React, { Fragment } from "react";
import { useTheme, Typography } from "@mui/material";
import { Polyline, Polygon, Tooltip } from "react-leaflet";
import { useTouchOnly } from "features/ui";

function AzbaSummary({ label, floor, ceiling }) {
  const props = {
    color: "secondary",
  };
  return (
    <Fragment>
      <Typography variant="subtitle2" {...props}>
        {label}
      </Typography>
      <Typography color="secondary" variant="body2" component="div">
        {`${floor} - ${ceiling}`}
      </Typography>
    </Fragment>
  );
}

function AzbaPolyline({ boundaries, hovered }) {
  const theme = useTheme();
  const color = theme.palette.error.main;
  const weight = hovered ? 3 : 1;

  const segments = boundaries
    ?.map((current, index, array) => {
      const next = index === array.length - 1 ? array[0] : array[index + 1];
      return current && next ? [current, next] : undefined;
    })
    ?.filter((segment) => segment);
  return (
    <Polyline
      key="boundaries"
      pathOptions={{
        color,
        weight,
      }}
      positions={segments}
    />
  );
}

export default function AzbaPolygon({
  boundaries,
  ceiling,
  floor,
  label,
  slug,
  hovered,
  onHover,
  ...props
}) {
  const touchOnly = useTouchOnly();
  const theme = useTheme();
  const fillOpacity = hovered ? 0.5 : 0.3;
  const color = hovered ? theme.palette.error.main : theme.palette.error.light;
  //color depends on ceiling ?

  const summary = <AzbaSummary ceiling={ceiling} floor={floor} label={label} />;

  return boundaries?.length > 0 ? (
    <Fragment>
      <Polygon
        weight={0}
        pathOptions={{
          color,
          fillColor: color,
          fillOpacity,
        }}
        positions={boundaries}
        eventHandlers={
          !touchOnly
            ? {
                mouseover: () => onHover(slug),
                mouseout: () => onHover(),
              }
            : {
                click: () => (hovered ? onHover() : onHover(slug)),
              }
        }
        {...props}
      >
        <Tooltip permanent={touchOnly && hovered} key={`${slug}-${hovered}`}>
          {summary}
        </Tooltip>
      </Polygon>
      <AzbaPolyline boundaries={boundaries} hovered={hovered} />
    </Fragment>
  ) : null;
}
