import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  CircularProgress,
  Stack,
  Divider,
} from "@mui/material";
import { TreeView, TreeItem } from "@mui/lab";
import { ChevronRight, ChevronDown } from "mdi-material-ui";
import { useSearchParamList, useSearchParams } from "features/router";
import {
  useFolderTreeQuery,
  useLayerList,
  OSM,
  GRAYSCALE,
} from "features/layers/hooks";
import { useDialog } from "features/ui";
import SelectAll from "../../../pages/FullscreenMap/OptionsMenu/GenericPickerDialog/SelectAll";
import SelectNone from "../../../pages/FullscreenMap/OptionsMenu/GenericPickerDialog/SelectNone";
import LayerTreeItemContent from "./LayerTreeItemContent";
import { useEffect } from "react";

//TODO (de) select an entire folder at once

function useTreeToggle(folders) {
  const first_level_folders = (f) => f?.data?.map(({ pk }) => `${pk}`) || [];
  const [expanded, setExpanded] = useState(first_level_folders(folders));

  const onToggle = (event, nodeIds) => {
    setExpanded(nodeIds);
  };

  useEffect(() => {
    if (folders) {
      //expand first level of folders
      setExpanded(first_level_folders(folders));
    }
  }, [folders]);

  return { expanded, onToggle };
}

function useTreeSelection(layers) {
  const [params, push] = useSearchParams();
  const selection = useSearchParamList("layers");

  const onSelect = (event, selected_item) => {
    const current_selection = layers
      ?.filter(({ slug }) => selection?.includes(slug))
      ?.map(({ slug }) => slug);
    let new_selection;
    if (current_selection?.includes(selected_item)) {
      new_selection = current_selection?.filter(
        (slug) => slug !== selected_item
      );
    } else {
      new_selection = [...(current_selection || []), selected_item];
    }
    push({ ...params, layers: new_selection?.join(",") });
  };

  const is_selected = (s) => selection?.includes(s);

  return { is_selected, onSelect };
}

export default function LayerTreePickerDialog() {
  const layers = useLayerList();
  const folders = useFolderTreeQuery();
  const { isOpen, open, close } = useDialog();

  const { expanded, onToggle } = useTreeToggle(folders);
  const { is_selected, onSelect } = useTreeSelection([
    ...(layers?.data || []),
    OSM,
    GRAYSCALE,
  ]);
  const isLoading = layers?.isLoading || folders?.isLoading;

  const renderTree = ({ pk, label, children, layers }) => (
    <TreeItem key={pk} nodeId={`${pk}`} label={label}>
      {children?.map((node) => renderTree(node))}
      {layers?.map((node) => renderLayer(node))}
    </TreeItem>
  );

  const renderLayer = ({ label, slug }) => (
    <TreeItem
      label={
        <LayerTreeItemContent label={label} selected={is_selected(slug)} />
      }
      nodeId={slug}
      key={slug}
    />
  );

  const display = (
    <Dialog open={isOpen} onClose={close}>
      <DialogTitle>Sélectionner les calques</DialogTitle>
      {folders?.data && (
        <DialogContent>
          <TreeView
            defaultCollapseIcon={<ChevronDown />}
            defaultExpandIcon={<ChevronRight />}
            defaultExpanded={folders?.data?.map(({ pk }) => `${pk}`)}
            expanded={expanded}
            onNodeToggle={onToggle}
            onNodeSelect={onSelect}
            sx={{
              "& .MuiTreeItem-content": {
                "&:hover": {
                  backgroundColor: (t) => t.palette.action.hover,
                },
                "&.Mui-focused, &.Mui-selected, &.Mui-selected.Mui-focused": {
                  backgroundColor: "transparent",
                  "&:hover": {
                    backgroundColor: (t) => t.palette.action.hover,
                  },
                },
              },
            }}
          >
            {folders?.data?.map((node) => renderTree(node))}
            {!folders?.data?.length &&
              folders?.isSuccess &&
              layers?.data?.map((node) => renderLayer(node))}
            {renderLayer(OSM)}
            {renderLayer(GRAYSCALE)}
          </TreeView>
        </DialogContent>
      )}
      <DialogActions>
        <Stack sx={{ flexGrow: 1 }}>
          <Divider flexItem />
          {!isLoading && (
            <Stack
              direction="row"
              justifyContent="flex-end"
              alignItems="center"
            >
              <SelectAll
                options={layers?.data?.map(({ slug }) => ({
                  pk: slug,
                }))}
                param_key="layers"
              />
              <SelectNone param_key="layers" />
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

  return { open, display };
}
