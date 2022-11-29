import { useMapEvents } from "react-leaflet";
import { useSearchParams } from "features/router";

export default function MapCallback() {
  const [params, push] = useSearchParams();

  const update_params = (mapEvents) => {
    const center = mapEvents.getCenter();
    push({
      ...params,
      zoom: mapEvents.getZoom(),
      center_lat: center?.lat,
      center_lon: center?.lng,
    });
  };

  const mapEvents = useMapEvents({
    zoomend: () => update_params(mapEvents),
    moveend: () => update_params(mapEvents),
  });

  return null;
}
