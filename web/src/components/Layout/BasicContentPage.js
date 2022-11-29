import React, { Fragment } from "react";
import { Container } from "@mui/material";
import InfoBox from "./InfoBox";

export default function BasicContentPage({ children }) {
  return (
    <Fragment>
      <Container
        maxWidth="lg"
        component="main"
        sx={{
          flexGrow: 1,
          minHeight: 0,
          overflowY: "auto",
          mt: 2,
          mb: 2,
        }}
      >
        {children}
      </Container>
      <InfoBox align="center" />
    </Fragment>
  );
}
