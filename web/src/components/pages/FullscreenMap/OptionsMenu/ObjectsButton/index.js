import React, { Fragment } from "react";
import {
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  CircularProgress,
  Badge,
} from "@mui/material";
import {
  ShapeOutline,
  Airport,
  RadioTower,
  MapMarkerCircle,
  Close,
  HexagonMultipleOutline,
  MapOutline,
} from "mdi-material-ui";
import { useInfo } from "features/info/hooks";
import useAirfieldPickerDialog from "./AirfieldPickerDialog";
import useSectorPickerDialog from "./SectorPickerDialog";
import useRadionavPickerDialog from "./RadionavPickerDialog";
import useAntennaPickerDialog from "./AntennaPickerDialog";
import useKmlPickerDialog from "./KMLPickerDialog";

export default function OptionsMenu() {
  const { radio_coverage_enabled } = useInfo();
  const airfield_dialog = useAirfieldPickerDialog();
  const sector_dialog = useSectorPickerDialog();
  const radionav_dialog = useRadionavPickerDialog();
  const antenna_dialog = useAntennaPickerDialog();
  const kml_dialog = useKmlPickerDialog();
  const actions = [
    {
      icon: <MapOutline />,
      name: "Cartes KML",
      dialog: kml_dialog,
    },
    ...(radio_coverage_enabled
      ? [
          {
            icon: <MapMarkerCircle />,
            name: "Couverture radio",
            dialog: antenna_dialog,
          },
        ]
      : []),
    {
      icon: <RadioTower />,
      name: "Moyens radionav",
      dialog: radionav_dialog,
    },
    {
      icon: <HexagonMultipleOutline />,
      name: "Secteurs",
      dialog: sector_dialog,
    },
    {
      icon: <Airport />,
      name: "Aérodromes",
      dialog: airfield_dialog,
    },
  ];
  return (
    <Fragment>
      <SpeedDial
        direction="left"
        icon={<SpeedDialIcon icon={<ShapeOutline />} openIcon={<Close />} />}
        FabProps={{ color: "default", size: "medium" }}
        ariaLabel="Menu carte"
      >
        {actions
          ?.filter(
            (action) =>
              action?.dialog?.available_count || action?.dialog?.isLoading
          )
          .map((action) => (
            <SpeedDialAction
              key={action.name}
              icon={
                <Badge
                  badgeContent={action?.dialog?.selection_count}
                  color="secondary"
                  max={9}
                >
                  {action?.dialog?.isLoading ? (
                    <CircularProgress size="24px" color="inherit" />
                  ) : (
                    action.icon
                  )}
                </Badge>
              }
              tooltipTitle={action.name}
              onClick={action?.dialog?.open}
            />
          ))}
      </SpeedDial>
      {airfield_dialog.display}
      {sector_dialog.display}
      {radionav_dialog.display}
      {antenna_dialog.display}
      {kml_dialog.display}
    </Fragment>
  );
}
