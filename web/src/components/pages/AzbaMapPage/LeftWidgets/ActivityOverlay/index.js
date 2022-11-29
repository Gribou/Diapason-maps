import React, { Fragment } from "react";
import { Paper, Stack, Typography, List } from "@mui/material";
import moment from "moment";
import { useSearchParams } from "features/router";
import AreaRow from "./AreaRow";

export default function ActivityOverlay({ active_areas, hovered, onHover }) {
  const [{ reference_date }] = useSearchParams();

  const known_areas = active_areas?.filter(
    ({ ceiling, floor }) => ceiling && floor
  );

  const unknown_areas = active_areas?.filter(
    ({ ceiling, floor }) => !ceiling || !floor
  );

  return (
    <Stack
      component={Paper}
      elevation={6}
      sx={{
        zIndex: 1050,
        overflow: "hidden",
        minHeight: 0,
        maxHeight: "100%",
      }}
    >
      {active_areas?.length > 0 ? (
        <Fragment>
          <Typography variant="h6" color="secondary" sx={{ px: 2, py: 1 }}>
            {reference_date
              ? `Activités le ${moment(reference_date, "YYYYMMDDHHmm").format(
                  "DD/MM/YYYY"
                )} à ${moment(reference_date, "YYYYMMDDHHmm").format(
                  "HH:mm"
                )} TU`
              : "Activités en cours"}
          </Typography>
          {unknown_areas?.length > 0 && (
            <List dense disablePadding sx={{ overflow: "auto" }}>
              {unknown_areas?.map((area) => (
                <AreaRow
                  key={area.slug}
                  {...area}
                  onHover={onHover}
                  hovered={hovered === area.slug}
                  warning
                />
              ))}
            </List>
          )}
          {known_areas?.length > 0 && (
            <List
              dense
              disablePadding
              onMouseLeave={() => onHover()}
              sx={{ overflow: "auto" }}
            >
              {known_areas?.map((area) => (
                <AreaRow
                  key={area.slug}
                  {...area}
                  onHover={onHover}
                  hovered={hovered === area.slug}
                />
              ))}
            </List>
          )}
        </Fragment>
      ) : (
        <Typography variant="h6" sx={{ p: 2 }} color="textSecondary">
          Aucune activité prévue en ce moment
        </Typography>
      )}
    </Stack>
  );
}
