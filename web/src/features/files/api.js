import { cleanSearchParam } from "features/utils";

export default (builder) => ({
  file: builder.query({
    query: (pk) => `files/file/${pk}/`,
  }),
  fileCategories: builder.query({
    query: () => "files/category/",
  }),
  searchFiles: builder.query({
    query: ({ search }) => ({
      url: "files/file/",
      params: { search: cleanSearchParam(search) },
    }),
  }),
});
