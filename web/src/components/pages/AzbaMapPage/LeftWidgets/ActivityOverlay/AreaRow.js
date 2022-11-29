import React from "react";
import {
  Stack,
  Typography,
  ListItem,
  ListItemButton,
  Tooltip,
  IconButton,
} from "@mui/material";
import { alpha } from "@mui/system";
import { AlertCircleOutline } from "mdi-material-ui";
import { useTouchOnly } from "features/ui";

export default function AreaRow({
  slug,
  label,
  floor,
  ceiling,
  warning,
  hovered,
  onHover,
}) {
  const touchOnly = useTouchOnly();
  return (
    <ListItem disablePadding>
      <Stack
        spacing={2}
        direction="row"
        alignItems="center"
        justifyContent="space-between"
        component={ListItemButton}
        onMouseEnter={() => !touchOnly && onHover(slug)}
        onClick={() => touchOnly && (hovered ? onHover() : onHover(slug))}
        selected={!warning && hovered}
        sx={
          warning
            ? {
                backgroundColor: (t) => alpha(t.palette.warning.light, 0.3),
                "&:hover": {
                  backgroundColor: (t) =>
                    alpha(
                      t.palette.warning.light,
                      0.3 + t.palette.action.selectedOpacity
                    ),
                },
              }
            : undefined
        }
      >
        <Typography>{label}</Typography>
        {!warning ? (
          <Typography variant="caption" color="textSecondary">
            {`${floor} - ${ceiling}`}
          </Typography>
        ) : (
          <Tooltip title="Les limites de cette zone ne sont pas connues.">
            <IconButton size="small" color="warning" sx={{ p: 0 }}>
              <AlertCircleOutline />
            </IconButton>
          </Tooltip>
        )}
      </Stack>
    </ListItem>
  );
}
