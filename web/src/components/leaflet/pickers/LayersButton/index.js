import React, { Fragment } from "react";
import { Fab, Tooltip } from "@mui/material";
import { LayersOutline } from "mdi-material-ui";

import useLayerTreePickerDialog from "./LayerTreePickerDialog";

export default function LayersButton() {
  const dialog = useLayerTreePickerDialog();
  return (
    <Fragment>
      <Tooltip title="Calques" placement="left">
        <Fab size="medium" onClick={dialog.open}>
          <LayersOutline />
        </Fab>
      </Tooltip>
      {dialog.display}
    </Fragment>
  );
}
