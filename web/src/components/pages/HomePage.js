import React, { Fragment } from "react";
import { Typography, Stack, Button, Link } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import CoconutsIcon from "components/logos/CoconutsIcon";
import SearchField from "components/misc/SearchField";
import { useHomepageQuery, getIconForCategory } from "features/nav/hooks";
import { URL_ROOT } from "constants";
import BasicContentPage from "components/Layout/BasicContentPage";

function HeroLogo() {
  return (
    <CoconutsIcon
      sx={{
        width: { xs: "3em", sm: "5em" },
        height: { xs: "3em", sm: "5em" },
        m: { xs: 0, sm: 1 },
        ml: 1,
        color: "secondary.dark",
      }}
    />
  );
}

function HeroContainer() {
  return (
    <Stack direction="row" sx={{ mt: { xs: 2, sm: 6 }, mb: { xs: 6, sm: 10 } }}>
      <HeroLogo />
      <Stack sx={{ px: 2 }}>
        <Typography
          variant="h2"
          component="h1"
          color="secondary"
          gutterBottom
          sx={{
            flexGrow: 1,
            typography: { xs: "h5", sm: "h3", md: "h2" },
          }}
        >
          Bienvenue sur Coconuts
        </Typography>
        <Typography
          sx={{
            maxWidth: "sm",
            typography: { xs: "body2", sm: "h6", md: "body1" },
          }}
          color="textSecondary"
          align="justify"
        >
          Vous trouverez ici les cartes et fréquences des aérodromes, les
          secteurs de contrôle et les moyens de radionavigation en-route pour le
          cycle AIRAC en cours.
        </Typography>
      </Stack>
    </Stack>
  );
}

function ShortcutButton({ label, category, url }) {
  const props = url?.includes("://")
    ? {
        href: url,
        target: "_blank",
        component: Link,
      }
    : {
        to: `${URL_ROOT}${url}`,
        component: RouterLink,
      };

  return (
    <Button
      startIcon={getIconForCategory(category)}
      color="secondary"
      sx={{ mx: 1 }}
      variant="outlined"
      size="large"
      {...props}
    >
      {label}
    </Button>
  );
}

export default function Home() {
  const { data: homepage } = useHomepageQuery();

  const search_field = (
    <Fragment>
      <SearchField
        placeholder="Entrez votre recherche ici"
        sx={{
          borderRadius: 1,
          bgcolor: (theme) => theme.palette.grey[300],
          "&:hover": {
            bgcolor: (theme) => theme.palette.grey[200],
          },
          maxWidth: "sm",
          color: "text.secondary",
        }}
      />
      <Typography align="center" variant="caption" color="textSecondary">
        (ex : lfpg sid, lfll iac 35, lfat, lflx vac, uj, p1, …)
      </Typography>
    </Fragment>
  );

  return (
    <BasicContentPage>
      <Stack alignItems="center" sx={{ maxWidth: "md", mx: "auto" }}>
        <HeroContainer />
        {search_field}

        {!!homepage?.length && (
          <Stack sx={{ alignItems: "center", mt: 12 }} direction="row">
            {homepage?.map(({ shortcut }, i) => (
              <ShortcutButton {...shortcut} key={i} />
            ))}
          </Stack>
        )}
      </Stack>
    </BasicContentPage>
  );
}
