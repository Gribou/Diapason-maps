import React from "react";
import { Button } from "@mui/material";
import { Phone, FileMultipleOutline } from "mdi-material-ui";
import { Link as RouterLink } from "react-router-dom";
import { useSearchMapsQuery } from "features/maps/hooks";
import { useSearchAirfieldsQuery } from "features/airfields/hooks";
import { useSearchSectorsQuery, useSearchAccQuery } from "features/acc/hooks";
import { useSearchTelephonesQuery } from "features/phones/hooks";
import { useSearchFilesQuery } from "features/files/hooks";
import { useSearchStationsQuery } from "features/radionav/hooks";
import {
  MapCard,
  AirfieldCard,
  SectorCard,
  PhoneCard,
  AccCard,
  FileCard,
  RadionavCard,
} from "components/items/ItemCards";
import { ROUTES } from "routes";
import ResultDisplay from "./ResultDisplay";

const MAX_DISPLAYED_AIRFIELDS = 6;
const MAX_DISPLAYED_SECTORS = 6;
const MAX_DISPLAYED_PHONES = 12;
const MAX_DISPLAYED_ACC = 6;
const MAX_DISPLAYED_FILES = 6;
const MAX_DISPLAYED_RADIONAV = 6;

export function useMapResults(params) {
  const query = useSearchMapsQuery(params);

  const display = (
    <ResultDisplay
      query={query}
      entityName="carte"
      CardComponent={MapCard}
      defaultExpanded={false}
    />
  );
  return {
    display,
    is_empty: !query?.data?.count,
    is_loading: query?.isLoading,
  };
}

export function useAirfieldResults(params) {
  const query = useSearchAirfieldsQuery(params);
  const is_empty = query?.isSuccess && !query?.data?.length;
  const is_unique = query?.isSuccess && query?.data?.length === 1;
  const unique_result_url = is_unique
    ? ROUTES.airfield.path.replace(":code", query?.data?.[0].icao_code)
    : undefined;

  const display = (
    <ResultDisplay
      query={query}
      entityName="aérodrome"
      max_displayed_count={MAX_DISPLAYED_AIRFIELDS}
      CardComponent={AirfieldCard}
    />
  );

  return {
    display,
    is_empty,
    is_loading: query?.isFetching,
    unique_result_url,
  };
}

export function useSectorResults(params) {
  const query = useSearchSectorsQuery(params);
  const is_empty = query?.isSuccess && !query?.data?.length;
  const is_unique = query?.isSuccess && query?.data?.length === 1;
  const unique_result_url = is_unique
    ? ROUTES.sector.path.replace(":sector_name", query?.data?.[0].name)
    : undefined;

  const display = (
    <ResultDisplay
      query={query}
      entityName="secteur"
      max_displayed_count={MAX_DISPLAYED_SECTORS}
      CardComponent={SectorCard}
    />
  );

  return {
    display,
    is_empty,
    unique_result_url,
    is_loading: query?.isFetching,
  };
}

export function useAccResults(params) {
  const query = useSearchAccQuery(params);
  const is_empty = query?.isSuccess && !query?.data?.length;
  const is_unique = query?.isSuccess && query?.data?.length === 1;
  const unique_result_url = is_unique;
  query?.isSuccess && query?.data?.length === 1
    ? ROUTES.acc.path.replace(":pk", query?.data?.[0].pk)
    : undefined;

  const display = (
    <ResultDisplay
      query={query}
      entityName="centre de contrôle"
      entityNamePlural="centres de contrôle"
      max_displayed_count={MAX_DISPLAYED_ACC}
      CardComponent={AccCard}
    />
  );

  return {
    display,
    is_empty,
    is_loading: query?.isFetching,
    unique_result_url,
  };
}

export function usePhoneResults(params) {
  const query = useSearchTelephonesQuery(params);
  const is_empty = query?.isSuccess && !query?.data?.length;

  const display = (
    <ResultDisplay
      query={query}
      entityName="téléphone"
      max_displayed_count={MAX_DISPLAYED_PHONES}
      CardComponent={PhoneCard}
      addOn={
        <Button
          component={RouterLink}
          startIcon={<Phone />}
          to={{ pathname: ROUTES.phones.path }}
          variant="outlined"
          sx={{ ml: "auto" }}
        >
          Annuaire
        </Button>
      }
    />
  );

  return { display, is_empty, is_loading: query?.isFetching };
}

export function useFilesResults(params) {
  const query = useSearchFilesQuery(params);
  const is_empty = query?.isSuccess && !query?.data?.length;

  const display = (
    <ResultDisplay
      query={query}
      entityName="autre"
      max_displayed_count={MAX_DISPLAYED_FILES}
      CardComponent={FileCard}
      addOn={
        <Button
          component={RouterLink}
          startIcon={<FileMultipleOutline />}
          to={{ pathname: ROUTES.files.path }}
          variant="outlined"
          sx={{ ml: "auto" }}
        >
          Tous les fichiers
        </Button>
      }
    />
  );

  return { display, is_empty, is_loading: query?.isFetching };
}

export function useStationsResults(params) {
  const query = useSearchStationsQuery(params);
  const is_empty = query?.isSuccess & !query?.data?.length;
  const is_unique = query?.isSuccess && query?.data?.length === 1;
  const unique_result_url = is_unique;
  query?.isSuccess && query?.data?.length === 1
    ? ROUTES.station.path.replace(":name", query?.data?.[0].short_name)
    : undefined;

  const display = (
    <ResultDisplay
      query={query}
      entityName="moyen radio"
      entityNamePlural="moyens radio"
      max_displayed_count={MAX_DISPLAYED_RADIONAV}
      CardComponent={RadionavCard}
    />
  );

  return {
    display,
    is_empty,
    is_loading: query?.isFetching,
    unique_result_url,
  };
}
