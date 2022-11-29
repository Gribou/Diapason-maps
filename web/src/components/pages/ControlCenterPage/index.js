import React from "react";
import { useParams } from "react-router-dom";
import { Typography, CircularProgress, Stack } from "@mui/material";
import { Radar } from "mdi-material-ui";
import BasicContentPage from "components/Layout/BasicContentPage";
import ItemCardList from "components/items/CollapsibleItemCardList";
import { useAccQuery } from "features/acc/hooks";
import { SectorCard } from "components/items/ItemCards";
import HeaderTitle from "components/misc/HeaderTitle";

export default function Sector() {
  const { pk } = useParams();
  const query = useAccQuery(pk);
  const { data: control_center, isLoading, isSuccess } = query;
  const { name, sectors } = control_center || {};

  const empty_display = isSuccess && !name && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Ce centre de contrôle n&apos;est pas dans la base de données.
    </Typography>
  );

  const sector_list = (
    <ItemCardList
      title="Secteurs"
      data={sectors?.filter((sector) => !sector.hidden)}
      CardComponent={SectorCard}
      size="large"
    />
  );

  return (
    <BasicContentPage>
      <Stack alignItems="stretch">
        {name && (
          <HeaderTitle title={name} Icon={Radar} sx={{ mb: 2, mt: 2 }} />
        )}
        {isLoading && (
          <CircularProgress
            color="secondary"
            sx={{ mt: 8, mx: "auto" }}
            size={60}
          />
        )}
        {sector_list}
        {empty_display}
      </Stack>
    </BasicContentPage>
  );
}
