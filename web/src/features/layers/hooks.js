import api from "features/api";

export const { useLayerListQuery, useFolderTreeQuery, useKmlListQuery } = api;

const make_tile_url_pretty = (url) =>
  url?.replace("$Z", "{z}")?.replace("$Y", "{y}")?.replace("$X", "{x}");

export function useLayerList() {
  const { data, ...rest } = useLayerListQuery();
  return {
    data: data?.map(({ tiles_url, ...layer }) => ({
      ...layer,
      tiles_url: make_tile_url_pretty(tiles_url),
    })),
    ...rest,
  };
}

export const OSM = {
  label: "OpenStreetMap",
  slug: "osm",
  tiles_url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  depth: -10,
  format: "png",
  metadata: {
    minzoom: 3,
    maxzoom: 12,
    attribution:
      '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
  },
};

export const GRAYSCALE = {
  label: "Nuances de gris",
  slug: "grayscale",
  tiles_url:
    "http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
  depth: -20,
  format: "png",
  metadata: {
    minzoom: 3,
    maxzoom: 12,
    attribution:
      'donn&eacute;es &copy; <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
  },
};
