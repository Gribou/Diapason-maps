import { useSearchParamList } from "features/router";
import { useSearchSectorsQuery } from "features/acc/hooks";
import useGenericPickerDialog from "../GenericPickerDialog";

function useSectorOptions() {
  const sector_list = useSearchParamList("sectors");
  const { data, isFetching } = useSearchSectorsQuery({});
  const options = data
    ?.filter(({ has_boundaries }) => has_boundaries)
    ?.map(({ name, control_center }) => ({
      selected: sector_list?.includes(name),
      pk: name,
      title: name,
      subtitle: control_center,
      metadata: [name, control_center?.replace("ACC", "")?.trim()]
        .join(" ")
        ?.toLowerCase(),
    }));
  return { options, isLoading: isFetching };
}

export default function useSectorPickerDialog() {
  const options = useSectorOptions();
  return useGenericPickerDialog({
    param_key: "sectors",
    title: "Sélectionner les secteurs en route",
    columnSize: 3,
    ...options,
  });
}
