import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { useMediaQuery, Link } from "@mui/material";
import ResponsiveButton from "components/misc/ResponsiveButton";
import { URL_ROOT } from "constants";
import { getIconForCategory } from "features/nav/hooks";

export default function ShortcutButton({ label, category, url, isLast }) {
  const xsDown = useMediaQuery((theme) => theme.breakpoints.down("xs"));

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
    <ResponsiveButton
      text={label}
      startIcon={getIconForCategory(category)}
      color="inherit"
      sx={{ mr: !isLast && { sm: 2 } }}
      edge={isLast ? "end" : undefined}
      size={!xsDown && "small"}
      {...props}
    />
  );
}
