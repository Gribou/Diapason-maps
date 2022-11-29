export default (builder) => ({
  schedule: builder.query({
    query: () => "civ/schedule/",
  }),
  azba: builder.query({
    query: (params) => ({
      url: "civ/azba/",
      params,
    }),
  }),
});
