import { useSearchParamList } from "features/router";
import { useSearchAirfieldsQuery } from "features/airfields/hooks";
import useGenericPickerDialog from "../GenericPickerDialog";

export function useAirfieldOptions() {
  const ad_list = useSearchParamList("ad");
  const { data, isFetching } = useSearchAirfieldsQuery({});
  const options = data?.map(({ icao_code, name }) => ({
    selected: ad_list?.includes(`${icao_code}`),
    pk: icao_code,
    title: icao_code,
    subtitle: name,
    metadata: [icao_code, name].join(" ")?.toLowerCase(),
  }));
  return { options, isLoading: isFetching };
}

export default function useAirfieldPickerDialog() {
  const options = useAirfieldOptions();
  return useGenericPickerDialog({
    param_key: "ad",
    title: "Sélectionner les aérodromes",
    columnSize: 3,
    ...options,
  });
}
