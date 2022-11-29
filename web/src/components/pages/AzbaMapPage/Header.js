import React from "react";
import moment from "moment";
import { Stack, Typography, Alert, Link } from "@mui/material";
import { ShieldAirplane } from "mdi-material-ui";
import { useInfo } from "features/info/hooks";
import HeaderTitle from "components/misc/HeaderTitle";

export default function Header({ isLoading, refetch }) {
  const { azba_schedule } = useInfo();
  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="stretch"
      sx={{ m: 1 }}
      spacing={2}
    >
      <HeaderTitle
        Icon={ShieldAirplane}
        loading={isLoading}
        refresh={refetch}
        title="AZBA"
        sx={{ flexGrow: 1 }}
      />
      {azba_schedule?.from ? (
        <Typography variant="subtitle2" color="secondary">
          {`Activités planifiées du RTBA du ${moment(azba_schedule?.from)
            .utc()
            .format("DD/MM/YYYY HH:mm TU")} au ${moment(azba_schedule?.up_to)
            .utc()
            .format("DD/MM/YYYY HH:mm TU")}`}
        </Typography>
      ) : (
        azba_schedule && (
          <Alert
            severity="error"
            variant="filled"
            component={Link}
            href="https://www.sia.aviation-civile.gouv.fr/schedules"
            sx={{
              textDecorationColor: "inherit",
            }}
          >
            Planification inconnue à ce jour. Consultez directement le SIA.
          </Alert>
        )
      )}
    </Stack>
  );
}
