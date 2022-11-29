import React from "react";
import {
  ListItem,
  ListItemText,
  ListItemButton,
  ListItemIcon,
} from "@mui/material";
import { CheckboxMultipleBlankOutline } from "mdi-material-ui";
import { useSearchParams } from "features/router";

export default function SelectNoneRow({ param_key }) {
  const [params, push] = useSearchParams();

  const onClick = () => {
    push({ ...params, [param_key]: undefined });
  };

  return (
    <ListItem>
      <ListItemButton role={undefined} onClick={onClick} dense>
        <ListItemIcon>
          <CheckboxMultipleBlankOutline />
        </ListItemIcon>
        <ListItemText
          primary="Tout dé-sélectionner"
          primaryTypographyProps={{ noWrap: true }}
        />
      </ListItemButton>
    </ListItem>
  );
}
