import { useSearchParamList } from "features/router";
import { useAntennasList } from "features/acc/hooks";
import useGenericPickerDialog from "../GenericPickerDialog";

function useAntennasOptions() {
  const pk_list = useSearchParamList("antennas");
  const { data, isFetching } = useAntennasList();
  const options = data?.map(({ pk, name }) => ({
    selected: pk_list?.includes(`${pk}`),
    pk,
    title: name,
    metadata: name,
  }));
  return { options, isLoading: isFetching };
}

export default function useAntennaPickerDialog() {
  const options = useAntennasOptions();
  return useGenericPickerDialog({
    param_key: "antennas",
    title: "Sélectionner les antennes radio",
    ...options,
  });
}
