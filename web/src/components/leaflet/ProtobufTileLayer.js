import { createTileLayerComponent, updateGridLayer } from "@react-leaflet/core";
import L from "leaflet";
import "leaflet.vectorgrid";

const VectorTileLayer = createTileLayerComponent(function createTileLayer(
  { url, style, ...options },
  context
) {
  return {
    instance: L.vectorGrid.protobuf(url, {
      rendererFactory: L.svg.tile,
      vectorTileLayerStyles: style || {},
      ...options,
    }),
    context,
  };
},
updateGridLayer);

export default VectorTileLayer;

// const url = "https://basemaps.arcgis.com/arcgis/rest/services/World_Basemap_v2/VectorTileServer/tile/{z}/{y}/{x}.pbf"
// <VectorTileLayer url={url} style={}/>
