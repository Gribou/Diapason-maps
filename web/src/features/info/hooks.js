import api from "features/api";

export const { useInfoQuery } = api;

export function useInfo() {
  const { data } = useInfoQuery();
  return data || {};
}
