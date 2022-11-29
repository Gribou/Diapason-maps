import api from "features/api";
import { useSearchParams } from "features/router";

export const { useScheduleQuery, useAzbaQuery } = api;

export function useActiveAzba(options) {
  const [{ reference_date }] = useSearchParams();
  return useAzbaQuery({ reference_date }, options);
}
