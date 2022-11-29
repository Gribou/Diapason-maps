import api from "features/api";
import { useInfo } from "features/info/hooks";

export const {
  useSectorQuery,
  useAccQuery,
  useSearchAccQuery,
  useSearchSectorsQuery,
  useAntennasQuery,
} = api;

export function useAntennasList() {
  const { data, ...rest } = useAntennasQuery();
  const { radio_coverage_enabled } = useInfo();
  return radio_coverage_enabled ? { data, ...rest } : rest;
}
