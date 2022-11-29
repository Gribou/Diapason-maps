import React from "react";
import { Typography, Container } from "@mui/material";
import BasicContentPage from "components/Layout/BasicContentPage";

export default function ErrorNotFound() {
  return (
    <BasicContentPage>
      <Container maxWidth="sm" sx={{ mt: 8 }}>
        <Typography variant="h4" color="secondary" align="center" gutterBottom>
          Page introuvable
        </Typography>
        <Typography variant="subtitle1" align="center">
          La page que vous cherchez n&apos;existe pas.
        </Typography>
      </Container>
    </BasicContentPage>
  );
}
