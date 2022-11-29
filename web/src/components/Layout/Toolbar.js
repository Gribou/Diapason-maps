import React from "react";
import { Link, Toolbar, IconButton, Box, Tooltip } from "@mui/material";
import { alpha } from "@mui/material/styles";
import { Link as RouterLink } from "react-router-dom";
import CoconutsIcon from "components/logos/CoconutsIcon";

import { ROUTES } from "routes";
import { DEBUG } from "constants";

import SearchField from "components/misc/SearchField";
import { useToolbarQuery } from "features/nav/hooks";
import { useInfo } from "features/info/hooks";
import ShortcutButton from "./ShortcutButton";

export default function MyToolbar() {
  const { data: shortcuts } = useToolbarQuery();
  const { version } = useInfo();

  const logo = (
    <Tooltip title={version || "version ?"}>
      <IconButton
        component={RouterLink}
        to={ROUTES.home.path}
        edge="start"
        color="inherit"
      >
        <CoconutsIcon baseColor="#fff" accentColor="#fff" fontSize="large" />
      </IconButton>
    </Tooltip>
  );

  const app_display = (
    <Link
      component={RouterLink}
      to={ROUTES.home.path}
      sx={{ mr: { sm: 2 }, display: { xs: "none", sm: "block" } }}
      variant="h5"
      underline="none"
      noWrap
      color="inherit"
    >{`Coconuts${DEBUG ? " Debug" : ""}`}</Link>
  );

  const search_field = (
    <Box
      sx={{
        position: "relative",
        ml: { xs: 0, sm: 3 },
        mr: 2,
        width: { xs: "100%", sm: "auto" },
        borderRadius: 1,
        color: (theme) => theme.palette.common.white,
        bgcolor: (theme) => alpha(theme.palette.common.white, 0.15),
        "&:hover": {
          bgcolor: (theme) => alpha(theme.palette.common.white, 0.25),
        },
      }}
    >
      <SearchField inputInputSx={{ width: { md: "20ch" } }} />
    </Box>
  );

  return (
    <Toolbar sx={{ color: "#fff" }}>
      {logo}
      {app_display}
      <Box sx={{ flexGrow: 1 }} />
      {search_field}
      {(shortcuts || [])?.map(({ shortcut }, i) => (
        <ShortcutButton
          key={i}
          {...shortcut}
          isLast={i === shortcuts?.length - 1}
        />
      ))}
    </Toolbar>
  );
}
