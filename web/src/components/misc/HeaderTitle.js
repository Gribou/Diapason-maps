import React from "react";
import {
  Stack,
  Typography,
  IconButton,
  CircularProgress,
  Tooltip,
} from "@mui/material";
import { Sync } from "mdi-material-ui";

function RefreshButton({ refresh, loading, size = "24px", ...props }) {
  return loading ? (
    <IconButton color="secondary" size="small" disabled {...props}>
      <CircularProgress size={size} color="secondary" />
    </IconButton>
  ) : (
    <Tooltip title="Actualiser">
      <IconButton color="secondary" size="small" onClick={refresh} {...props}>
        <Sync color="secondary" />
      </IconButton>
    </Tooltip>
  );
}

export default function HeaderTitle({
  Icon,
  title,
  subtitle,
  comment,
  addOn,
  loading,
  refresh,
  ...props
}) {
  return (
    <Stack direction="row" alignItems="baseline" {...props}>
      <Icon fontSize="large" sx={{ mr: 2 }} color="secondary" />
      {title && (
        <Typography
          component="span"
          sx={{ mr: 1, typography: { xs: "h5", sm: "h4" } }}
          color="secondary"
        >
          {title}
        </Typography>
      )}
      {subtitle && (
        <Typography
          component="span"
          variant="h6"
          color="secondary"
          sx={{ mr: 1 }}
          noWrap
        >
          {subtitle}
        </Typography>
      )}
      {comment && (
        <Typography
          component="span"
          color="secondary"
          variant="subtitle2"
          noWrap
        >
          {comment}
        </Typography>
      )}
      {(refresh || loading) && (
        <RefreshButton
          sx={{ alignSelf: "center" }}
          color="inherit"
          loading={loading}
          refresh={refresh}
        />
      )}
      {addOn}
    </Stack>
  );
}
