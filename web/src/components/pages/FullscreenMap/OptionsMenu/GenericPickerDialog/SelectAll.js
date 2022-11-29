import React from "react";
import {
  ListItem,
  ListItemText,
  ListItemButton,
  ListItemIcon,
} from "@mui/material";
import { CheckboxMultipleMarkedOutline } from "mdi-material-ui";
import { useSearchParams } from "features/router";

export default function SelectAllRow({ options, param_key }) {
  const [params, push] = useSearchParams();

  const onClick = () => {
    const current_selection = params?.[param_key]?.split(",") || [];
    const new_selection = [
      ...current_selection,
      ...(options?.map(({ pk }) => pk) || []),
    ];
    push({ ...params, [param_key]: [...new Set(new_selection)]?.join(",") });
  };

  return (
    <ListItem>
      <ListItemButton role={undefined} onClick={onClick} dense>
        <ListItemIcon>
          <CheckboxMultipleMarkedOutline />
        </ListItemIcon>
        <ListItemText
          primary="Tout sélectionner"
          primaryTypographyProps={{ noWrap: true }}
        />
      </ListItemButton>
    </ListItem>
  );
}
