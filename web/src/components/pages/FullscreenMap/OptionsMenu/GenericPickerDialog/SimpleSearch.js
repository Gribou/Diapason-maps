import React, { useState } from "react";
import { TextField, InputAdornment, IconButton } from "@mui/material";
import { Close, Magnify } from "mdi-material-ui";

export function metadata_has_keywords(keywords, metadata) {
  const keyword_list = keywords?.toLowerCase().split(" ");
  return keyword_list?.every((k) => metadata?.toLowerCase()?.includes(`${k}`));
}

export default function useSimpleSearch() {
  const [keyword, setKeyword] = useState("");

  const handleBlur = () => {
    setKeyword((v) => v.trim());
  };

  const handleInput = (e) => {
    setKeyword(e.target.value);
  };

  const clear = () => {
    setKeyword("");
  };

  const display = (
    <TextField
      variant="outlined"
      size="small"
      margin="dense"
      color="secondary"
      value={keyword || ""}
      onBlur={handleBlur}
      onChange={handleInput}
      placeholder="Recherche..."
      sx={{ mr: 2 }}
      InputProps={{
        sx: { pr: 0 },
        endAdornment: (
          <InputAdornment position="end">
            <IconButton
              onClick={clear}
              size="small"
              color="secondary"
              disabled={!keyword}
            >
              <Close />
            </IconButton>
          </InputAdornment>
        ),
        startAdornment: (
          <InputAdornment position="start">
            <Magnify />
          </InputAdornment>
        ),
      }}
    />
  );

  return { keyword, display };
}
