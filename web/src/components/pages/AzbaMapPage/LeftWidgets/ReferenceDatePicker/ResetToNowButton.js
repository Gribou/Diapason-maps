import React from "react";
import { Tooltip, IconButton } from "@mui/material";
import { Replay } from "mdi-material-ui";
import { now } from "./utils";

export default function ResetToNowButton({ onSubmit }) {
  return (
    <Tooltip title="Maintenant">
      <IconButton size="small" onClick={() => onSubmit(now())}>
        <Replay />
      </IconButton>
    </Tooltip>
  );
}
