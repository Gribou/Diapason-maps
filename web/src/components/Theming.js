import React from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { green } from "@mui/material/colors";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";

const theme = createTheme({
  palette: {
    primary: green,
    secondary: { main: "#3b8386" },
  },
});

const Theming = ({ children }) => (
  <ThemeProvider theme={theme}>{children}</ThemeProvider>
);

export default Theming;
