import React, { Fragment } from "react";
import {
  useCeilingAndFloorFromSearchParams,
  useSearchParamList,
} from "features/router";
import { useAntennasQuery } from "features/acc/hooks";
import LocationMarker from "components/leaflet/LocationMarker";
import RangeCircle from "components/leaflet/RangeCircle";
import { ANTENNA_ICON } from "components/leaflet/icons";

export function useAntennasFromSearchParams() {
  const pk_list = useSearchParamList("antennas");
  const { data } = useAntennasQuery();
  return data?.filter(({ pk }) => pk_list?.includes(`${pk}`));
}

export default function Antennas() {
  const { ceiling } = useCeilingAndFloorFromSearchParams();
  const antennas = useAntennasFromSearchParams();
  return (
    <Fragment>
      {(antennas || [])
        ?.filter((antenna) => antenna?.latitude && antenna?.longitude)
        ?.map((antenna) => (
          <Fragment key={antenna?.pk}>
            <LocationMarker {...antenna} base64icon={ANTENNA_ICON} />
            <RangeCircle {...antenna} altitude={ceiling} />
          </Fragment>
        ))}
    </Fragment>
  );
}
