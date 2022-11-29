import { cleanSearchParam } from "features/utils";

export default (builder) => ({
  map: builder.query({
    query: (pk) => `airfields/map/${pk}/`,
  }),
  searchMaps: builder.query({
    query: ({ search }) => ({
      url: "airfields/map/",
      params: { search: cleanSearchParam(search) },
    }),
  }),
});
