import React from "react";
import moment from "moment";
import { Typography, Link, Skeleton, Stack, Container } from "@mui/material";
import { useInfoQuery } from "features/info/hooks";
import ErrorBox from "components/misc/ErrorBox";

export default function InfoBox({ sx = [], ...props }) {
  const { data: info, isLoading, error, isError } = useInfoQuery();
  const {
    up_to_date,
    displayed_airac,
    map_count,
    airfield_count,
    sector_count,
    station_count,
  } = info || {};

  const get_message = () => {
    if (displayed_airac) {
      return `AIRAC ${!up_to_date ? "PERIME " : ""}${moment(
        displayed_airac,
        "YYYY-MM-DD"
      ).format("DD/MM/YYYY")} - ${airfield_count || "?"} aérodromes - ${
        map_count || "?"
      } cartes - ${sector_count || "?"} secteurs - ${
        station_count || "?"
      } moyens radionav`;
    } else {
      return `${airfield_count || "?"} aérodromes - ${
        map_count || "?"
      } cartes - ${sector_count || "?"} secteurs - ${
        station_count || "?"
      } moyens radionav`;
    }
  };

  return isLoading ? (
    <Skeleton sx={sx} />
  ) : isError ? (
    <ErrorBox errorDict={error} sx={sx} {...props} />
  ) : (
    <Container maxWidth="lg" {...props}>
      <Stack direction="row" justifyContent="space-between">
        <Typography
          color={!up_to_date ? "error" : "textSecondary"}
          sx={[{ typography: "caption" }, ...(Array.isArray(sx) ? sx : [sx])]}
          noWrap
        >
          {get_message()}
        </Typography>
        <Typography
          color={!up_to_date ? "error" : "textSecondary"}
          sx={[{ typography: "caption" }, ...(Array.isArray(sx) ? sx : [sx])]}
          {...props}
          noWrap
        >
          <Link
            href="https://www.sia.aviation-civile.gouv.fr"
            rel="noopener noreferrer"
            target="_blank"
          >
            SIA
          </Link>
          {" - "}
          <Link
            href="https://ops.skeyes.be/html/belgocontrol_static/eaip/eAIP_Main/html/index-en-GB.html"
            rel="noopener noreferrer"
            target="_blank"
          >
            Skeyes.be
          </Link>
          {" - "}
          <Link
            href="https://aip.dfs.de/basicIFR/"
            rel="noopener noreferrer"
            target="_blank"
          >
            DFS
          </Link>
          {" - "}
          <Link
            href="https://www.aurora.nats.co.uk/web/guest/aip-products1"
            rel="noopener noreferrer"
            target="_blank"
          >
            NATS
          </Link>
        </Typography>
      </Stack>
    </Container>
  );
}
