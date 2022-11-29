import { useSearchParamList } from "features/router";
import { useSearchStationsQuery } from "features/radionav/hooks";
import useGenericPickerDialog from "../GenericPickerDialog";

function useStationOptions() {
  const station_list = useSearchParamList("radio");
  const { data, isFetching } = useSearchStationsQuery({});
  const options = data?.map(({ short_name, long_name }) => ({
    selected: station_list?.includes(`${short_name}`),
    pk: short_name,
    title: short_name,
    subtitle: long_name,
    metadata: [short_name, long_name].join(" ")?.toLowerCase(),
  }));
  return { options, isLoading: isFetching };
}

export default function useStationPickerDialog() {
  const options = useStationOptions();
  return useGenericPickerDialog({
    param_key: "radio",
    title: "Sélectionner les moyens de radionavigation",
    columnSize: 3,
    ...options,
  });
}
