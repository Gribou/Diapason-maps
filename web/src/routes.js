import React from "react";
import { URL_ROOT } from "constants";

import {
  HomePage,
  ResultsPage,
  AirfieldPage,
  ErrorPage,
  SectorPage,
  PhoneListPage,
  ControlCenterPage,
  FileListPage,
  CivListPage,
  FullscreenMap,
  StationPage,
  AzbaMapPage,
} from "components/pages";

export const ROUTES = {
  home: {
    path: `${URL_ROOT}/`,
    element: <HomePage />,
  },
  results: {
    path: `${URL_ROOT}/search`,
    element: <ResultsPage />,
  },
  airfield: {
    path: `${URL_ROOT}/airfield/:code`,
    element: <AirfieldPage />,
  },
  sector: {
    path: `${URL_ROOT}/sector/:sector_name`,
    element: <SectorPage />,
  },
  station: {
    path: `${URL_ROOT}/radionav/:name`,
    element: <StationPage />,
  },
  acc: {
    path: `${URL_ROOT}/acc/:pk`,
    element: <ControlCenterPage />,
  },
  phones: {
    path: `${URL_ROOT}/telephones`,
    element: <PhoneListPage />,
  },
  files: {
    path: `${URL_ROOT}/files`,
    element: <FileListPage />,
  },
  azba: {
    path: `${URL_ROOT}/azba`,
    element: <AzbaMapPage />,
  },
  civ: {
    path: `${URL_ROOT}/civ`,
    element: <CivListPage />,
  },
  map: {
    path: `${URL_ROOT}/map`,
    element: <FullscreenMap />,
  },
  error404: {
    path: "*",
    element: <ErrorPage />,
  },
};
