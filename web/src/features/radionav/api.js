import { cleanSearchParam } from "features/utils";

export default (builder) => ({
  station: builder.query({
    query: (name) => ({
      url: `radionav/station/${name?.toUpperCase()}/`,
    }),
  }),
  searchStations: builder.query({
    query: ({ search }) => ({
      url: "radionav/station/",
      params: { search: cleanSearchParam(search) },
    }),
  }),
});
