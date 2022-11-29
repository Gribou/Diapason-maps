import React from "react";
import { Typography, CircularProgress, Stack, Grid } from "@mui/material";
import { useScheduleQuery } from "features/civ/hooks";
import BasicContentPage from "components/Layout/BasicContentPage";
import CivSummary from "./CivSummary";

export default function CivListPage() {
  const { data, isLoading, isSuccess } = useScheduleQuery();

  const empty_display = isSuccess && !data?.length && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Aucun horaire disponible
    </Typography>
  );

  const loading_display = isLoading && (
    <CircularProgress color="secondary" sx={{ mt: 8, mx: "auto" }} size={60} />
  );

  const pln_phone_number = (
    <Typography
      sx={{ mx: "auto", mt: 6, mb: 2, border: 1, borderRadius: 2, p: 2 }}
      color="secondary"
      variant="h5"
    >
      Clôture des plans de vol : 01 56 301 301
    </Typography>
  );

  return (
    <BasicContentPage>
      <Stack alignItems="stretch">
        {loading_display}
        {empty_display}
        <Grid container spacing={3} justifyContent="center" alignItems="center">
          {data?.map((civ, i) => (
            <Grid item key={i} xs={3}>
              <CivSummary {...civ} />
            </Grid>
          ))}
        </Grid>
        {pln_phone_number}
      </Stack>
    </BasicContentPage>
  );
}
