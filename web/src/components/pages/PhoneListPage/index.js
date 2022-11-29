import React from "react";
import { CircularProgress, Typography, Stack } from "@mui/material";
import { Phone } from "mdi-material-ui";
import ErrorBox from "components/misc/ErrorBox";
import HeaderTitle from "components/misc/HeaderTitle";
import BasicContentPage from "components/Layout/BasicContentPage";
import { useTelephonesQuery } from "features/phones/hooks";
import { useTab } from "features/ui";
import PhoneCategoryTab from "./PhoneListTab";
import PhoneTabsHeader from "./PhoneTabsHeader";

const TABS = [
  { title: "CDS", value: "isCDS" },
  { title: "Zone Est", value: "isE" },
  { title: "Zone Ouest", value: "isW" },
];
//FIXME make this configurable in backend

export default function Telephones() {
  const {
    isLoading,
    isSuccess,
    error,
    data: categories,
  } = useTelephonesQuery();
  const noData = isSuccess && !categories?.length;
  const { tab, onChange } = useTab(TABS[0].value);

  const loading_display = isLoading && (
    <CircularProgress color="secondary" sx={{ mt: 8, mx: "auto" }} size={60} />
  );

  const empty_display = noData && (
    <Typography color="textSecondary" align="center" sx={{ m: 4 }}>
      Aucun numéro dans la base de données.
    </Typography>
  );

  return (
    <BasicContentPage>
      <Stack alignItems="stretch">
        <HeaderTitle
          Icon={Phone}
          title="Annuaire téléphonique"
          sx={{ mb: 2, mt: 2 }}
          alignItems="center"
        />
        <PhoneTabsHeader tab={tab} onChange={onChange} config={TABS} />
        {loading_display}
        <ErrorBox errorDict={error} />
        <PhoneCategoryTab categories={categories} tab={tab} />
        {empty_display}
      </Stack>
    </BasicContentPage>
  );
}
