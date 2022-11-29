import React, { Fragment } from "react";
import { useSearchSectorsQuery } from "features/acc/hooks";
import SectorArtefact from "components/leaflet/SectorArtefact";
import {
  useSearchParamList,
  useCeilingAndFloorFromSearchParams,
} from "features/router";

function useSectorsFromSearchParams() {
  const sector_list = useSearchParamList("sectors");
  const { data } = useSearchSectorsQuery({});
  return data?.filter(({ name }) => sector_list?.includes(name));
}

export default function Sectors() {
  const { ceiling, floor } = useCeilingAndFloorFromSearchParams();
  const sectors = useSectorsFromSearchParams();

  return (
    <Fragment>
      {(sectors || [])
        ?.filter((sector) => sector?.parts)
        ?.map(({ name, parts, control_center }) => (
          <SectorArtefact
            name={name}
            parts={parts}
            key={name}
            clickable
            ceiling={ceiling}
            floor={floor}
            control_center={control_center}
          />
        ))}
    </Fragment>
  );
}
