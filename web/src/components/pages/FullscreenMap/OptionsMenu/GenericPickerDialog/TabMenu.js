import React from "react";
import { Tab, Tabs } from "@mui/material";
import { useTab } from "features/ui";

export default function useTabMenu(counts) {
  const { tab, onChange } = useTab("all");

  const display = (
    <Tabs
      value={tab}
      onChange={onChange}
      indicatorColor="secondary"
      textColor="secondary"
      sx={{
        borderBottom: 1,
        borderColor: "divider",
      }}
    >
      <Tab
        label={`Tout${counts ? ` (${counts?.all || 0})` : ""}`}
        value="all"
      />
      <Tab
        label={`Sélection${counts ? ` (${counts?.selection || 0})` : ""}`}
        value="selection"
      />
    </Tabs>
  );

  return { tab, display };
}
