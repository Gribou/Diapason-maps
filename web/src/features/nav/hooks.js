import React from "react";
import api from "features/api";
import {
  EarthBox,
  Airport,
  RadioTower,
  Phone,
  Radar,
  FileMultipleOutline,
  Home,
  ShieldAirplane,
  ClockOutline,
} from "mdi-material-ui";

export const { useHomepageQuery, useToolbarQuery } = api;

export function getIconForCategory(category) {
  switch (category) {
    case "AIRFIELD":
      return <Airport />;
    case "MAP":
      return <EarthBox />;
    case "SECTOR":
      return <Radar />;
    case "PHONE":
      return <Phone />;
    case "RADIO":
      return <RadioTower />;
    case "FILE":
      return <FileMultipleOutline />;
    case "AZBA":
      return <ShieldAirplane />;
    case "HOME":
      return <Home />;
    case "SCHEDULE":
      return <ClockOutline />;
  }
}
