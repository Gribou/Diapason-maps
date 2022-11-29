import React, { useState, Fragment } from "react";
import moment from "moment";
import { Tooltip, IconButton } from "@mui/material";
import { Calendar } from "mdi-material-ui";
import { MobileDateTimePicker } from "@mui/x-date-pickers";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { useDialog } from "features/ui";
import { to_timestamp } from "./utils";

const timestamp_to_moment = (t) => moment.unix(t).utc();

function DateTimePickerDialog({ isOpen, min, max, close, value, setValue }) {
  const [pending, setPending] = useState(timestamp_to_moment(value));

  return (
    <LocalizationProvider
      dateAdapter={AdapterMoment}
      instance={moment}
      adapterLocale="fr-FR"
      localeText={{
        cancelButtonLabel: "Annuler",
        okButtonLabel: "OK",
        clearButtonLabel: "Vider",
      }}
    >
      <MobileDateTimePicker
        open={isOpen}
        onClose={close}
        onOpen={() => setPending(value)}
        value={pending}
        onChange={setPending}
        onAccept={(v) => setValue(to_timestamp(v))}
        toolbarTitle="Sélectionner date et heure TU"
        toolbarFormat="DD MMM"
        renderInput={() => null}
        minDateTime={timestamp_to_moment(min)}
        maxDateTime={timestamp_to_moment(max)}
        componentsProps={{
          actionBar: {
            actions: ["clear", "accept", "cancel"],
          },
        }}
      />
    </LocalizationProvider>
  );
}

export default function DateTimePickerButton({
  defaultValue,
  min,
  max,
  onSubmit,
}) {
  const { isOpen, open, close } = useDialog();
  return (
    <Fragment>
      <Tooltip title="Autre choix">
        <IconButton size="small" onClick={open}>
          <Calendar />
        </IconButton>
      </Tooltip>
      <DateTimePickerDialog
        value={defaultValue}
        setValue={onSubmit}
        isOpen={isOpen}
        close={close}
        min={min}
        max={max}
      />
    </Fragment>
  );
}
