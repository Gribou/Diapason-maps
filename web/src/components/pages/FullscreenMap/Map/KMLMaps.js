import React, { Fragment } from "react";
import { useApiCall } from "features/api";
import { useSearchParamList } from "features/router";
import { useKmlListQuery } from "features/layers/hooks";
import KMLMapLayer from "components/leaflet/KMLMapLayer";

function useKmlsFromSearchParams() {
  const pk_list = useSearchParamList("kml");
  const { data } = useKmlListQuery();
  return data?.filter(({ pk }) => pk_list?.includes(`${pk}`));
}

function KMLMap({ url }) {
  const { data } = useApiCall(url) || {};
  if (data) {
    try {
      const parser = new DOMParser();
      return <KMLMapLayer kml={parser.parseFromString(data, "text/xml")} />;
    } catch (e) {
      console.warn(e);
    }
  }
  return null;
}

export default function KMLMaps() {
  const maps = useKmlsFromSearchParams();
  return (
    <Fragment>
      {maps?.map(({ kml_file, pk }) => (
        <KMLMap url={kml_file} key={pk} />
      ))}
    </Fragment>
  );
}
