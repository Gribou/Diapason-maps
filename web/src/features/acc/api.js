import { cleanSearchParam } from "features/utils";

export default (builder) => ({
  antennas: builder.query({
    query: () => "acc/antenna/",
  }),
  sector: builder.query({
    query: (name) => `acc/sector/${name}/`,
  }),
  searchSectors: builder.query({
    query: ({ search, ...params }) => ({
      url: "acc/sector/",
      params: { search: cleanSearchParam(search), ...params },
    }),
  }),
  acc: builder.query({
    query: (pk) => `acc/control_center/${pk}/`,
  }),
  searchAcc: builder.query({
    query: ({ search }) => ({
      url: "acc/control_center/",
      params: { search: cleanSearchParam(search) },
    }),
  }),
});
