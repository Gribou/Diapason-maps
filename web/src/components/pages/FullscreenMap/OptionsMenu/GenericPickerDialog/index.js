import React, { useEffect } from "react";
import {
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  Button,
  CircularProgress,
  Grid,
  Divider,
  Stack,
  Typography,
} from "@mui/material";
import { useDialog } from "features/ui";
import OptionRow from "./OptionRow";
import SelectAll from "./SelectAll";
import SelectNone from "./SelectNone";
import usePaginator from "./Paginator";
import useSimpleSearch, { metadata_has_keywords } from "./SimpleSearch";
import useTabMenu from "./TabMenu";

const useFilters = ({ options, tab, page_size }) => {
  const search = useSimpleSearch();
  const filter_content = (s) =>
    s?.filter(
      ({ metadata }) =>
        !search?.keyword || metadata_has_keywords(search.keyword, metadata)
    );
  const selection = filter_content(
    tab === "selection" ? options?.filter(({ selected }) => selected) : options
  );

  const paginator = usePaginator({
    count: selection?.length || 0,
    pageSize: page_size,
  });

  useEffect(() => {
    paginator.setPage(1);
  }, [search.keyword]);

  const display = (selection?.length >= page_size || search.keyword) && (
    <Stack justifyContent="flex-end" alignItems="center" direction="row">
      {search.display}
      <Typography sx={{ flexGrow: 1 }}>{`${selection?.length} éléments${
        search.keyword ? ` (sur ${options?.length})` : ""
      }`}</Typography>
      {paginator.display}
    </Stack>
  );

  return {
    display,
    selection,
    current_page: selection?.slice(
      (paginator.page - 1) * page_size,
      paginator.page * page_size
    ),
  };
};

export default function GenericPickerDialog({
  options,
  isLoading,
  param_key,
  title,
  columnSize = true,
  page_size = 24,
}) {
  const { isOpen, open, close } = useDialog();
  const menu = useTabMenu({
    all: options?.length,
    selection: options?.filter(({ selected }) => selected)?.length,
  });
  const filters = useFilters({ options, tab: menu.tab, page_size });

  const display = (
    <Dialog open={isOpen} onClose={close} fullWidth maxWidth="md">
      <DialogTitle>{title}</DialogTitle>
      {options?.length >= page_size && (
        <DialogContent sx={{ flex: "0 0 auto", pb: 1, pt: 0 }}>
          {menu.display}
          {filters.display}
        </DialogContent>
      )}
      <DialogContent sx={{ flex: "1 1 auto", py: 1 }}>
        <Grid container>
          {filters.selection?.length === 0 && (
            <Grid item xs={12} sx={{ justifyContent: "center" }}>
              <Typography color="text.secondary">Aucun élément</Typography>
            </Grid>
          )}
          {filters.current_page?.map((item) => (
            <Grid item key={item?.pk} xs={columnSize}>
              <OptionRow {...item} options={options} param_key={param_key} />
            </Grid>
          ))}
        </Grid>
      </DialogContent>
      <DialogActions>
        <Stack sx={{ flexGrow: 1 }}>
          <Divider flexItem />
          {!isLoading && (
            <Stack
              direction="row"
              justifyContent="flex-end"
              alignItems="center"
            >
              {menu.tab !== "selection" && (
                <SelectAll options={filters.selection} param_key={param_key} />
              )}
              <SelectNone param_key={param_key} />
            </Stack>
          )}
          <Stack direction="row" justifyContent="flex-end" alignItems="center">
            {isLoading && <CircularProgress size={24} color="secondary" />}
            <Button onClick={close} color="secondary">
              Fermer
            </Button>
          </Stack>
        </Stack>
      </DialogActions>
    </Dialog>
  );

  return {
    open,
    display,
    isLoading,
    available_count: options?.length,
    selection_count: options?.filter(({ selected }) => selected)?.length,
  };
}
