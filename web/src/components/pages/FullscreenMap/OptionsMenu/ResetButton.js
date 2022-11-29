import React from "react";
import { Fab, Tooltip } from "@mui/material";
import { Replay } from "mdi-material-ui";
import { useSearchParams } from "features/router";

export default function ResetAction() {
  const [, push] = useSearchParams();
  const onClick = () => {
    push({});
    window.location.reload(false);
  };

  return (
    <Tooltip title="Réinitialiser la carte" placement="left">
      <Fab onClick={onClick} size="medium">
        <Replay />
      </Fab>
    </Tooltip>
  );
}
