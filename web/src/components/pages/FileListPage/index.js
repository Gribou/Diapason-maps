import React from "react";
import { Typography, Stack, CircularProgress } from "@mui/material";
import { FileMultipleOutline } from "mdi-material-ui";
import { useInfo } from "features/info/hooks";
import { useFileCategoriesQuery } from "features/files/hooks";

import BasicContentPage from "components/Layout/BasicContentPage";
import HeaderTitle from "components/misc/HeaderTitle";
import ItemCardList from "components/items/CollapsibleItemCardList";
import { FileCard } from "components/items/ItemCards";

export default function FileListPage() {
  const { files_enabled } = useInfo();
  const { data, isLoading, isSuccess } = useFileCategoriesQuery();

  const empty_display = files_enabled && isSuccess && !data?.length && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Aucun fichier disponible
    </Typography>
  );

  const forbidden_display = !isLoading && !files_enabled && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Cette fonctionnalité est désactivée
    </Typography>
  );

  const loading_display = isLoading && (
    <CircularProgress color="secondary" sx={{ mt: 8, mx: "auto" }} size={60} />
  );

  return (
    <BasicContentPage>
      <Stack alignItems="stretch">
        <HeaderTitle
          title="Autres fichiers"
          Icon={FileMultipleOutline}
          sx={{ mb: 4, mt: 2 }}
        />
        {loading_display}
        {forbidden_display}
        {empty_display}
        {files_enabled &&
          data?.map(({ label, files }, i) => (
            <ItemCardList
              key={i}
              title={label}
              data={files}
              CardComponent={FileCard}
              size="large"
            />
          ))}
      </Stack>
    </BasicContentPage>
  );
}
