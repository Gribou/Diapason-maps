export default (builder) => ({
  homepage: builder.query({
    query: () => "nav/homepage/",
  }),
  toolbar: builder.query({
    query: () => "nav/toolbar/",
  }),
});
