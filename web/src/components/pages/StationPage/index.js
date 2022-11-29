import React from "react";
import { useParams } from "react-router-dom";
import { Typography, CircularProgress, Stack } from "@mui/material";

import BasicContentPage from "components/Layout/BasicContentPage";
import { useStationQuery } from "features/radionav/hooks";
import Header from "./Header";

export default function StationPage() {
  const { name } = useParams();
  const query = useStationQuery(name);
  const { data: station, isLoading, isSuccess } = query;

  const empty_display = isSuccess && !station?.short_name && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Ce moyen de radionavigation n&apos;est pas dans la base de données.
    </Typography>
  );

  const loading_display = isLoading && (
    <CircularProgress color="secondary" sx={{ mt: 8, mx: "auto" }} size={60} />
  );

  const header = station?.short_name && <Header {...(station || {})} />;

  return (
    <BasicContentPage>
      <Stack>
        {loading_display}
        {header}
        {empty_display}
      </Stack>
    </BasicContentPage>
  );
}
