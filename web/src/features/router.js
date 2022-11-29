import {
  useSearchParams as useRouterSearchParams,
  createSearchParams as createRouterSearchParams,
} from "react-router-dom";

export const useSearchParams = () => {
  const [params, push] = useRouterSearchParams();
  return [
    Object.fromEntries(params),
    (p) =>
      push(Object.fromEntries(Object.entries(p)?.filter(([, value]) => value))),
  ];
};

export const createSearchParams = (params) =>
  createRouterSearchParams(
    Object.fromEntries(Object.entries(params)?.filter(([, value]) => value))
  );

export const useSearchParamList = (key) => {
  const [params] = useSearchParams();
  return params?.[key]?.split(",");
};

export const useCeilingAndFloorFromSearchParams = () => {
  const [{ ceiling, floor }] = useSearchParams();
  const max_alt = parseInt(ceiling, 10) || 400;
  const min_alt = parseInt(floor, 10) || 0;
  return { ceiling: max_alt, floor: min_alt };
};
