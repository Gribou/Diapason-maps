import React from "react";
import { Navigate } from "react-router-dom";
import { Stack, Typography } from "@mui/material";
import { Magnify } from "mdi-material-ui";
import { useSearchParams } from "features/router";
import HeaderTitle from "components/misc/HeaderTitle";
import BasicContentPage from "components/Layout/BasicContentPage";
import { useInfo } from "features/info/hooks";
import {
  useMapResults,
  useAirfieldResults,
  useSectorResults,
  usePhoneResults,
  useAccResults,
  useFilesResults,
  useStationsResults,
} from "./Results";

const useResults = (params) => {
  const results = {
    airfields: useAirfieldResults(params),
    maps: useMapResults(params),
    sectors: useSectorResults(params),
    phones: usePhoneResults(params),
    acc: useAccResults(params),
    stations: useStationsResults(params),
    files: useFilesResults(params),
  };

  const non_empty_results = Object.values(results)?.filter(
    ({ is_empty }) => !is_empty
  );
  //auto redirect to the unique result if there is only one for all entities

  return {
    ...results,
    unique_result_url:
      non_empty_results.length === 1
        ? non_empty_results[0].unique_result_url
        : undefined,
  };
};

export default function Results() {
  const [params] = useSearchParams();
  const { phones_enabled, files_enabled } = useInfo();
  const results = useResults(params);

  return results?.unique_result_url ? (
    <Navigate to={results?.unique_result_url} replace />
  ) : (
    <BasicContentPage>
      <Stack alignItems="stretch">
        <HeaderTitle
          Icon={Magnify}
          title={`Résultats pour "${params?.search}"`}
          sx={{ mb: 4, mt: 2 }}
          alignItems="center"
          // addOn={
          //   <Button
          //     component={RouterLink}
          //     startIcon={<Earth />}
          //     to={{
          //       pathname: ROUTES.map.path,
          //       search: createSearchParams(params).toString(),
          //     }}
          //     variant="outlined"
          //     sx={{ ml: "auto" }}
          //   >
          //     Carte des résultats
          //   </Button>
          // }
        />
        {results?.airfields?.display}
        {results?.sectors?.display}
        {results?.stations?.display}
        {results?.acc?.display}
        {results?.maps?.display}
        {phones_enabled && results?.phones?.display}
        {files_enabled && results?.files?.display}
        <Typography
          variant="subtitle2"
          color="textSecondary"
          align="right"
          gutterBottom
          sx={{ mt: 2 }}
        >
          Utilisez des critères de recherche plus précis si vous n&apos;avez pas
          trouvé votre bonheur.
        </Typography>
      </Stack>
    </BasicContentPage>
  );
}
