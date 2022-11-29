import "leaflet-kml";
import * as L from "leaflet";
import { createLayerComponent } from "@react-leaflet/core";
import { useEffect } from "react";

const updateOnCanvas = (map) => {
  if (map.options.preferCanvas) {
    map._renderer._update();
  }
};

const createLeafletElement = (props, context) => {
  useEffect(() => {
    return () => {
      updateOnCanvas(context.map);
    };
  }, []);

  const { kml, kmlOptions } = props;
  const instance = new L.KML(kml, kmlOptions);
  if (context.map.options.preferCanvas) {
    setTimeout(
      (map) => {
        // Handling react-leaflet bug of canvas renderer not updating
        map._renderer._update();
      },
      0,
      context.map
    );
  }
  return { instance, context };
};

const updateLeafletElement = (instance) => {
  updateOnCanvas(instance._map);
};

export default createLayerComponent(createLeafletElement, updateLeafletElement);
