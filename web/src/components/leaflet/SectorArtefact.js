import React, { Fragment } from "react";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import { useTheme, Typography, Link } from "@mui/material";
import { Polyline, Polygon, Tooltip, Popup } from "react-leaflet";
import { useTouchOnly } from "features/ui";
import { ROUTES } from "routes";

function SectorPolyline({ boundaries, highlight }) {
  const theme = useTheme();
  const color = highlight
    ? theme.palette.primary.main
    : theme.palette.secondary.main;
  const weight = highlight ? 4 : 2;

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

function SectorSummary({ name, floor, ceiling, control_center, clickable }) {
  const Component = clickable ? Link : Typography;
  const props = clickable
    ? {
        component: RouterLink,
        to: ROUTES.sector.path.replace(":sector_name", name),
      }
    : {
        color: "secondary",
      };
  return (
    <Fragment>
      <div>
        <Component variant="subtitle2" {...props}>
          {name}
        </Component>
      </div>
      <Typography color="secondary" variant="body2" component="div">
        {control_center}
      </Typography>
      <Typography color="secondary" variant="body2" component="div">
        {`${floor} - ${ceiling}`}
      </Typography>
    </Fragment>
  );
}

function SectorPolygon({
  boundaries,
  ceiling,
  floor,
  name,
  control_center,
  highlight,
  single,
  clickable,
  ...props
}) {
  const navigate = useNavigate();
  const touchOnly = useTouchOnly();
  const theme = useTheme();
  const fillOpacity = highlight ? 0.3 : single ? 0.2 : 0.1;
  const color = highlight
    ? theme.palette.primary.main
    : theme.palette.secondary.main;

  const summary = (
    <SectorSummary
      ceiling={ceiling}
      floor={floor}
      name={name}
      control_center={control_center}
      clickable={clickable && touchOnly}
    />
  );

  return (
    <Polygon
      key="background"
      weight={0}
      pathOptions={{
        color,
        fillColor: color,
        fillOpacity,
      }}
      positions={boundaries}
      eventHandlers={{
        click: () =>
          clickable &&
          !touchOnly &&
          navigate(ROUTES.sector.path.replace(":sector_name", name)),
      }}
      {...props}
    >
      {touchOnly ? (
        <Popup closeButton={false}>{summary}</Popup>
      ) : (
        <Tooltip sticky permanent={highlight} key={`${name}-${highlight}`}>
          {summary}
        </Tooltip>
      )}
    </Polygon>
  );
}

export default function SectorArtefact({
  parts,
  name,
  control_center,
  highlight,
  clickable,
  ceiling,
  floor,
}) {
  const is_part_relevant = ({ ceiling: c, floor: f }) => {
    //only show parts of sector that overlap floor-ceiling range from args
    if (ceiling < floor || (!ceiling && !floor)) {
      return true;
    }
    const parsed_ceiling = parseInt(c.replace("FL", "").trim(), 10) || 0;
    const parsed_floor = parseInt(f.replace("FL", "").trim(), 10) || 0;
    if (parsed_floor <= floor) {
      return parsed_ceiling >= floor;
    }
    return parsed_floor <= ceiling;
  };

  return (
    <Fragment>
      {parts
        ?.filter((part) => is_part_relevant(part))
        ?.map((part, i) => (
          <Fragment key={part?.pk}>
            <SectorPolyline
              {...part}
              highlight={highlight === true || part?.pk === highlight}
            />
            <SectorPolygon
              name={name}
              control_center={control_center}
              {...part}
              single={parts?.length <= 1}
              highlight={
                (highlight === true && i === 0) || part?.pk === highlight
              }
              clickable={clickable}
            />
          </Fragment>
        ))}
    </Fragment>
  );
}
