import React from "react";
import { useState } from "react";
import {
  Collapse,
  IconButton,
  Typography,
  Grid,
  Stack,
  Link,
} from "@mui/material";
import { ChevronDown } from "mdi-material-ui";

const SMALL_CONFIG = { xs: 6, sm: 4, md: 3 };
const LARGE_CONFIG = { xs: 12, sm: 6, md: 4 };

function ItemCardGrid({ data, size, CardComponent, sx }) {
  return (
    <Grid
      container
      spacing={{ xs: 1, sm: 3 }}
      justify="flex-start"
      alignItems="stretch"
      sx={sx}
    >
      {data.map(
        (elt, i) =>
          elt && (
            <Grid item {...size} key={i}>
              <CardComponent item={elt} sx={{ height: "100%" }} />
            </Grid>
          )
      )}
    </Grid>
  );
}

export default function CollapsibleItemCardList({
  data = [],
  title,
  CardComponent,
  size = "small",
  display_count = 8,
}) {
  const config = size === "large" ? LARGE_CONFIG : SMALL_CONFIG;
  const [open, setOpen] = useState(false);

  const button_collapse = data.length > display_count && (
    <IconButton onClick={() => setOpen(!open)} color="secondary">
      <ChevronDown
        style={{
          transform: open ? "rotate(-180deg)" : "",
          transition: "transform 150ms ease", // smooth transition
        }}
      />
    </IconButton>
  );

  const header_display = (
    <Stack direction="row" alignItems="center" justifyContent="space-between">
      <Typography sx={{ ml: 1 }} color="textSecondary" variant="button">
        {title}
      </Typography>
      {button_collapse}
    </Stack>
  );

  const data_display_short = data.length > 0 && (
    <ItemCardGrid
      size={config}
      CardComponent={CardComponent}
      data={data?.slice(0, display_count)}
      sx={{ mt: 1 }}
    />
  );

  const data_display_collapse = data.length >= display_count && (
    <Collapse in={open} sx={{ mt: 2 }}>
      <ItemCardGrid
        size={config}
        CardComponent={CardComponent}
        data={data?.slice(display_count)}
      />
    </Collapse>
  );

  const other_cards = data.length >= display_count && !open && (
    <Link textAlign="right" onClick={() => setOpen(!open)}>
      ...et {data.length - display_count} autres.
    </Link>
  );

  return (
    data?.length > 0 && (
      <Stack sx={{ mb: 4, ml: 0, flexGrow: 1 }}>
        {header_display}
        {data_display_short}
        {data_display_collapse}
        {other_cards}
      </Stack>
    )
  );
}
