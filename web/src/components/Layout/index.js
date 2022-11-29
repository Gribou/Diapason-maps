import React from "react";
import { Outlet } from "react-router-dom";
import { CssBaseline, AppBar, Toolbar, Stack } from "@mui/material";

import CustomToolbar from "./Toolbar";

export default function Layout() {
  return (
    <Stack
      sx={{
        //do not use 100vh for Safari else bottom bar is out of screen
        //but Chrome does not handle fill-available properly either so should use 100vh
        //https://allthingssmitty.com/2020/05/11/css-fix-for-100vh-in-mobile-webkit/
        minHeight: "100vh",
        "@supports (-webkit-touch-callout: none)": {
          //Safari only https://browserstrangeness.bitbucket.io/css_hacks.html#safari
          minHeight: "-webkit-fill-available",
        },
      }}
      direction="column"
      alignItems="stretch"
      justifyContent="center"
    >
      <CssBaseline />
      <AppBar>
        <CustomToolbar />
      </AppBar>
      <Toolbar />
      <Outlet />
    </Stack>
  );
}
