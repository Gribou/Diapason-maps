import React, { Fragment } from "react";
import { Tooltip, Popup } from "react-leaflet";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { Typography, Link } from "@mui/material";

import { useTouchOnly } from "features/ui";
import { useSearchParamList } from "features/router";
import { useSearchStationsQuery } from "features/radionav/hooks";
import { ROUTES } from "routes";
import { RADIO_TOWER_ICON } from "components/leaflet/icons";
import LocationMarker from "components/leaflet/LocationMarker";

function StationSummary({ short_name, types, long_name, clickable }) {
  const Component = clickable ? Link : Typography;
  const props = clickable
    ? {
        component: RouterLink,
        to: ROUTES.station.path.replace(":name", short_name),
      }
    : {
        color: "secondary",
      };
  return (
    <Fragment>
      <div>
        <Component variant="subtitle2" {...props}>
          {`${short_name} (${[...types].reverse().join("-")})`}
        </Component>
      </div>
      <Typography color="secondary" variant="body2" component="span">
        {long_name}
      </Typography>
    </Fragment>
  );
}

function StationMarker({ highlight, ...station }) {
  const touchOnly = useTouchOnly();
  const navigate = useNavigate();
  const { latitude, longitude, short_name } = station;

  const summary = <StationSummary {...station} clickable={touchOnly} />;
  const eventHandlers = {
    click: () => navigate(ROUTES.station.path.replace(":name", short_name)),
  };

  return (
    <LocationMarker
      base64icon={RADIO_TOWER_ICON}
      latitude={latitude}
      longitude={longitude}
      eventHandlers={!touchOnly ? eventHandlers : undefined}
    >
      {touchOnly ? (
        <Popup closeButton={false}>{summary}</Popup>
      ) : (
        <Tooltip
          sticky
          permanent={highlight}
          key={`${short_name}-${highlight}`}
        >
          {summary}
        </Tooltip>
      )}
    </LocationMarker>
  );
}

function useStationsFromSearchParams() {
  const radio_list = useSearchParamList("radio");
  const { data } = useSearchStationsQuery({});
  return data?.filter(({ short_name }) => radio_list?.includes(short_name));
}

export default function Stations() {
  const stations = useStationsFromSearchParams();

  return (
    <Fragment>
      {(stations || [])
        ?.filter((station) => station?.latitude && station?.longitude)
        ?.map((station) => (
          <StationMarker key={station?.short_name} {...station} />
        ))}
    </Fragment>
  );
}
