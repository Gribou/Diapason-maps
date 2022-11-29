import React, { Fragment } from "react";
import { Tooltip, Popup } from "react-leaflet";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import { Typography, Link } from "@mui/material";
import { useSearchAirfieldsQuery } from "features/airfields/hooks";
import { useTouchOnly } from "features/ui";
import { useSearchParamList } from "features/router";
import { ROUTES } from "routes";
import { AIRFIELD_ICON } from "components/leaflet/icons";
import LocationMarker from "components/leaflet/LocationMarker";

function AirfieldSummary({ icao_code, name, clickable }) {
  const Component = clickable ? Link : Typography;
  const props = clickable
    ? {
        component: RouterLink,
        to: ROUTES.airfield.path.replace(":code", icao_code),
      }
    : {
        color: "secondary",
      };
  return (
    <Fragment>
      <div>
        <Component variant="subtitle2" {...props}>
          {icao_code}
        </Component>
      </div>
      <Typography color="secondary" variant="body2" component="span">
        {name}
      </Typography>
    </Fragment>
  );
}

function AirfieldMarker(airfield) {
  const touchOnly = useTouchOnly();
  const navigate = useNavigate();
  const { latitude, longitude, icao_code } = airfield;

  const summary = <AirfieldSummary {...airfield} clickable={touchOnly} />;
  const eventHandlers = {
    click: () => navigate(ROUTES.airfield.path.replace(":code", icao_code)),
  };

  return (
    <LocationMarker
      base64icon={AIRFIELD_ICON}
      latitude={latitude}
      longitude={longitude}
      eventHandlers={!touchOnly ? eventHandlers : undefined}
    >
      {touchOnly ? (
        <Popup closeButton={false}>{summary}</Popup>
      ) : (
        <Tooltip sticky key={icao_code}>
          {summary}
        </Tooltip>
      )}
    </LocationMarker>
  );
}

function useAirfieldsFromSearchParams() {
  const ad_list = useSearchParamList("ad");
  const { data } = useSearchAirfieldsQuery({});
  return data?.filter(({ icao_code }) => ad_list?.includes(icao_code));
}

export default function Airfields() {
  const airfields = useAirfieldsFromSearchParams();

  return (
    <Fragment>
      {(airfields || [])
        ?.filter((airfield) => airfield?.latitude && airfield?.longitude)
        ?.map((airfield) => (
          <AirfieldMarker key={airfield?.icao_code} {...airfield} />
        ))}
    </Fragment>
  );
}
