import React, { useState } from "react";
import { Stack, Box } from "@mui/material";

import { useActiveAzba } from "features/civ/hooks";
import Header from "./Header";
import Map from "./Map";
import LeftWidgets from "./LeftWidgets";
import RightWidgets from "./RightWidgets";

export default function AzbaMap() {
  const { data, refetch, isLoading } = useActiveAzba({
    pollingInterval: 3 * 60 * 1000, //3 min
  });
  const [hovered, setHovered] = useState();

  //FIXME instead of polling, compute is_active on frontend depending on schedule ?

  return (
    <Stack
      sx={{
        flexGrow: 1,
        height: 0,
        position: "relative",
        overscrollBehavior: "contain",
        touchAction: "none",
      }}
    >
      <Header isLoading={isLoading} refetch={refetch} />
      <Box sx={{ flexGrow: 1 }}>
        <Map active_areas={data} hovered={hovered} onHover={setHovered} />
      </Box>
      <RightWidgets />
      <LeftWidgets active_areas={data} hovered={hovered} onHover={setHovered} />
    </Stack>
  );
}
