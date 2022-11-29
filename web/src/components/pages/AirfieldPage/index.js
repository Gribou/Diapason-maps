import React from "react";
import { useParams } from "react-router-dom";
import { CircularProgress, Typography, Stack } from "@mui/material";
import { useAirfieldQuery } from "features/airfields/hooks";
import { useInfo } from "features/info/hooks";
import {
  MapCard,
  FrequencyCard,
  PhoneCard,
  FileCard,
} from "components/items/ItemCards";
import ItemCardList from "components/items/CollapsibleItemCardList";
import BasicContentPage from "components/Layout/BasicContentPage";
import AirfieldHeader from "./Header";

export default function Airfield() {
  const { code } = useParams();
  const { phones_enabled, files_enabled } = useInfo();
  const query = useAirfieldQuery(code);
  const { data: airfield, isLoading } = query;
  const { name, maps, phones, frequencies, files } = airfield || {};

  const loading_display = isLoading && (
    <CircularProgress color="secondary" sx={{ mt: 8, mx: "auto" }} size={60} />
  );

  const empty_display = !isLoading && !name && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Cet aérodrome n&apos;est pas dans la base de données.
    </Typography>
  );

  const header = name && <AirfieldHeader {...(airfield || {})} />;

  const map_list = maps && (
    <ItemCardList
      data={maps}
      title="Cartes (AIP)"
      CardComponent={MapCard}
      size="large"
      display_count={6}
    />
  );

  const freq_list = frequencies && (
    <ItemCardList
      data={frequencies}
      title="Fréquences (AIP)"
      CardComponent={FrequencyCard}
      size="large"
      display_count={6}
    />
  );

  const phone_list = phones_enabled && (
    <ItemCardList
      data={phones}
      title="Téléphones"
      CardComponent={PhoneCard}
      size="large"
      display_count={6}
    />
  );

  const files_list = files_enabled && (
    <ItemCardList
      data={files}
      title="Autres"
      CardComponent={FileCard}
      size="large"
      display_count={6}
    />
  );

  return (
    <BasicContentPage>
      <Stack>
        {header}
        {loading_display}
        {freq_list}
        {map_list}
        {phone_list}
        {files_list}
        {empty_display}
      </Stack>
    </BasicContentPage>
  );
}
