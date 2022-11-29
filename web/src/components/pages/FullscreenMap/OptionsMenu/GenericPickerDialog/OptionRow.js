import React from "react";
import {
  ListItem,
  ListItemText,
  ListItemButton,
  ListItemIcon,
  Checkbox,
} from "@mui/material";
import { useSearchParams } from "features/router";

export default function OptionRow({
  pk,
  selected,
  title,
  subtitle,
  options,
  param_key,
}) {
  const [params, push] = useSearchParams();

  const onSelect = (selected_item) => {
    const current_selection = options
      ?.filter(({ selected }) => selected)
      ?.map(({ pk }) => pk);
    let new_selection;
    if (current_selection?.includes(selected_item)) {
      //remove selected_item from selection
      new_selection = current_selection?.filter((pk) => pk !== selected_item);
    } else {
      //add selected_item to selection
      new_selection = [...(current_selection || []), selected_item];
    }
    push({ ...params, [param_key]: new_selection?.join(",") });
  };
  return (
    <ListItem disablePadding>
      <ListItemButton role={undefined} onClick={() => onSelect(pk)} dense>
        <ListItemIcon>
          <Checkbox
            edge="start"
            checked={selected || false}
            tabIndex={-1}
            disableRipple
            color="secondary"
          />
        </ListItemIcon>
        <ListItemText
          primaryTypographyProps={{ noWrap: true }}
          primary={title}
          secondary={subtitle}
        />
      </ListItemButton>
    </ListItem>
  );
}
