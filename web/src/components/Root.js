import React from "react";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";
import { ErrorBoundary } from "react-error-boundary";
import { Alert } from "@mui/material";

import Theming from "./Theming";
import Routing from "./Routing";

function Fallback({ error }) {
  return <Alert severity="error">{error.message}</Alert>;
}

export default function Root({ store }) {
  return (
    <ErrorBoundary FallbackComponent={Fallback}>
      <Provider store={store}>
        <Theming>
          <BrowserRouter>
            <Routing />
          </BrowserRouter>
        </Theming>
      </Provider>
    </ErrorBoundary>
  );
}
