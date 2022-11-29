import React, { Fragment } from "react";
import { Pane, TileLayer } from "react-leaflet";
import ProtobufTileLayer from "components/leaflet/ProtobufTileLayer";
import { useSearchParamList } from "features/router";
import { useLayerList, OSM, GRAYSCALE } from "features/layers/hooks";

function useLayersFromSearchParams() {
  const slug_list = useSearchParamList("layers");
  const { data } = useLayerList();
  return [
    ...(data?.filter(({ slug }) => slug_list?.includes(slug)) || []),
    ...(slug_list?.includes("osm") ? [OSM] : []),
    ...(slug_list?.includes("grayscale") || !slug_list?.length
      ? [GRAYSCALE]
      : []),
  ];
}

export default function Layers() {
  const layers = useLayersFromSearchParams();
  if (
    layers &&
    layers?.find(({ format }) => !["png", "pbf"].includes(format))
  ) {
    console.warn("Only PNG and PBF layers are supported.");
  }

  return (
    <Fragment>
      {layers?.map(({ tiles_url, slug, metadata, format, style, depth }) => (
        <Pane name={slug} key={slug} style={{ zIndex: 100 + depth }}>
          {format === "png" && (
            <TileLayer
              url={tiles_url}
              minZoom={metadata?.minzoom}
              maxZoom={metadata?.maxzoom}
            />
          )}
          {format === "pbf" && (
            <ProtobufTileLayer
              url={tiles_url}
              minZoom={metadata?.minzoom}
              maxZoom={metadata?.maxzoom}
              style={style}
            />
          )}
        </Pane>
      ))}
      {/* <ProtobufTileLayer url="https://basemaps.arcgis.com/arcgis/rest/services/World_Basemap_v2/VectorTileServer/tile/{z}/{y}/{x}.pbf" /> */}
    </Fragment>
  );
}
