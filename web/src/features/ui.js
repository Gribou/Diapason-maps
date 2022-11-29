import { useMediaQuery } from "@mui/material";
import { useState, useEffect } from "react";

export function useDialog() {
  const [isOpen, setOpen] = useState(false);

  const open = () => setOpen(true);

  const close = () => setOpen(false);

  return { isOpen, open, close };
}

export function useTab(default_value = 0) {
  const [tab, setTab] = useState(default_value);

  const onChange = (e, new_tab) => setTab(new_tab);

  return { tab, onChange };
}

export function useTouchOnly() {
  //touch devices are not hoverable
  return useMediaQuery("@media (hover: none), (pointer: coarse)");
}

export function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay || 500);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}
