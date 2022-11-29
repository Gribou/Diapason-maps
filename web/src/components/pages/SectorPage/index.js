import React from "react";
import { useParams } from "react-router-dom";
import { Typography, CircularProgress, Stack } from "@mui/material";
import { PhoneCard, FileCard } from "components/items/ItemCards";
import ItemCardList from "components/items/CollapsibleItemCardList";
import BasicContentPage from "components/Layout/BasicContentPage";
import { useSectorQuery } from "features/acc/hooks";
import { useInfo } from "features/info/hooks";
import SectorHeader from "./SectorHeader";

export default function Sector() {
  const { sector_name } = useParams();
  const { phones_enabled, files_enabled } = useInfo();
  const query = useSectorQuery(sector_name);
  const { data: sector, isLoading, isSuccess } = query;
  const { name, phones, files } = sector || {};

  const empty_display = isSuccess && !name && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Ce secteur n&apos;est pas dans la base de données.
    </Typography>
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

  const header = <SectorHeader {...sector} />;

  const loading_display = isLoading && (
    <CircularProgress color="secondary" sx={{ mt: 8, mx: "auto" }} size={60} />
  );

  return (
    <BasicContentPage>
      <Stack>
        {header}
        {loading_display}
        {phone_list}
        {files_list}
        {empty_display}
      </Stack>
    </BasicContentPage>
  );
}
