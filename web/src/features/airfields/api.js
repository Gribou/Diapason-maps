import { cleanSearchParam } from "features/utils";

export default (builder) => ({
  airfield: builder.query({
    query: (icao_code) => ({
      url: `airfields/airfield/${icao_code?.toUpperCase()}/`,
      params: { search: cleanSearchParam(icao_code) },
    }),
  }),
  searchAirfields: builder.query({
    query: ({ search, ...params }) => ({
      url: "airfields/airfield/",
      params: {
        ...params,
        search: cleanSearchParam(search),
      },
    }),
  }),
});
