import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { IconButton, Input, InputAdornment } from "@mui/material";
import { Magnify, Close } from "mdi-material-ui";
import { ROUTES } from "routes";
import { createSearchParams, useSearchParams } from "features/router";

export default function SearchField({
  placeholder = "Recherche…",
  sx,
  inputInputSx,
  ...props
}) {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [keyword, setKeyword] = useState(params.search || "");

  useEffect(() => {
    //update field value when location changes (ex : filters are cleared)
    setKeyword(params.search || "");
  }, [params.search]);

  const handleBlur = () => {
    setKeyword((v) => v.trim());
  };

  const handleInput = (e) => {
    setKeyword(e.target.value);
  };

  const clear = () => {
    setKeyword("");
  };

  const handleKeyUp = (e) => {
    if (e.charCode === 13 || e.key === "Enter") {
      handleSearchRequest(keyword);
    } else if (e.charCode === 27 || e.key === "Escape") {
      clear();
    }
  };

  const handleSearchRequest = (keyword) => {
    navigate({
      pathname: ROUTES.results.path,
      search: createSearchParams({ search: keyword }).toString(),
    });
  };

  return (
    <Input
      placeholder={placeholder}
      sx={{
        color: "inherit",
        "& .MuiInput-input": {
          p: 1,
          pl: {
            xs: "1em",
            sm: (theme) => `calc(1em + ${theme.spacing(2)}px)`,
            transition: (theme) => theme.transitions.create("width"),
            ...inputInputSx,
          },
        },
        ...sx,
      }}
      autoComplete="off"
      inputProps={{ "aria-label": "search" }}
      onBlur={handleBlur}
      onChange={handleInput}
      onKeyUp={handleKeyUp}
      value={keyword || ""}
      disableUnderline
      endAdornment={
        <InputAdornment position="end" sx={{ color: "inherit" }}>
          <IconButton
            onClick={() => handleSearchRequest(keyword)}
            size="small"
            color="inherit"
          >
            <Magnify />
          </IconButton>
          {keyword && (
            <IconButton onClick={clear} size="small" color="inherit">
              <Close />
            </IconButton>
          )}
        </InputAdornment>
      }
      fullWidth
      {...props}
    />
  );
}
