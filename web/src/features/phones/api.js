import { cleanSearchParam } from "features/utils";

export default (builder) => ({
  telephones: builder.query({
    query: () => "phones/category/",
  }),
  searchTelephones: builder.query({
    query: ({ search }) => ({
      url: "phones/phone/",
      params: { search: cleanSearchParam(search) },
    }),
  }),
});
