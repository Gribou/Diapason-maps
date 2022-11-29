import React from "react";
import { Tabs, Tab } from "@mui/material";

export default function PhoneTabsHeader({ tab, onChange, config }) {
  return (
    <Tabs
      value={tab}
      onChange={onChange}
      indicatorColor="primary"
      sx={{ borderBottom: 1, borderColor: "divider", mb: 2 }}
    >
      {config.map(({ title, value }) => (
        <Tab key={value} label={title} value={value} />
      ))}
    </Tabs>
  );
}
