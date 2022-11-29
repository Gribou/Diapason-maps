import { useSearchParamList } from "features/router";
import { useKmlListQuery } from "features/layers/hooks";
import useGenericPickerDialog from "../GenericPickerDialog";

function useKmlOptions() {
  const pk_list = useSearchParamList("kml");
  const { data, isFetching } = useKmlListQuery();
  const options = data?.map(({ pk, label }) => ({
    selected: pk_list?.includes(`${pk}`),
    pk,
    title: label,
    metadata: label?.toLowerCase(),
  }));
  return { options, isLoading: isFetching };
}

export default function useKmlPickerDialog() {
  const options = useKmlOptions();
  return useGenericPickerDialog({
    param_key: "kml",
    title: "Sélectionner les cartes KML",
    ...options,
  });
}
