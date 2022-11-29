import React from "react";
import { Stack } from "@mui/material";
import { PhoneCard } from "components/items/ItemCards";
import ItemCardList from "components/items/CollapsibleItemCardList";

export default function PhoneListTab({ categories, tab }) {
  //filter displayed phones according to selected tab
  return (
    <Stack>
      {categories?.map(({ name, telephones }, i) => (
        <ItemCardList
          key={i}
          title={name}
          data={telephones?.filter((phone) => phone[tab])}
          CardComponent={PhoneCard}
        />
      ))}
    </Stack>
  );
}
