export default (builder) => ({
  layerList: builder.query({
    query: () => "layers/layer/",
  }),
  folderTree: builder.query({
    query: () => "layers/folder/",
  }),
  kmlList: builder.query({
    query: () => "layers/kml/",
  }),
});
