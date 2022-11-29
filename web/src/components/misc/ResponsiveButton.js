import React from "react";
import { IconButton, Button, Tooltip, useMediaQuery } from "@mui/material";

export default function ResponsiveButton({
  text,
  tooltipText,
  startIcon,
  endIcon,
  ...props
}) {
  const smUp = useMediaQuery((theme) => theme.breakpoints.up("sm"));
  return (
    <Tooltip title={tooltipText || (smUp ? "" : text)} arrow>
      <span>
        {smUp ? (
          <Button
            variant="outlined"
            startIcon={startIcon}
            endIcon={endIcon}
            style={{ whiteSpace: "nowrap" }}
            {...props}
          >
            {text}
          </Button>
        ) : (
          <IconButton {...props}>{startIcon || endIcon}</IconButton>
        )}
      </span>
    </Tooltip>
  );
}
