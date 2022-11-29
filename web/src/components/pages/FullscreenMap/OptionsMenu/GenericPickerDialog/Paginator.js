import React, { useState } from "react";
import { Pagination, PaginationItem } from "@mui/material";

export default function usePaginator({ count, pageSize = 30 }) {
  const [page, setPage] = useState(1);
  const nb_pages = () => Math.floor((count - 1) / pageSize) + 1;

  const display =
    nb_pages() > 1 ? (
      <Pagination
        count={nb_pages()}
        color="secondary"
        page={parseInt(page, 10) || 1}
        onChange={(e, value) => setPage(value)}
        renderItem={(item) => (
          <PaginationItem
            {...item}
            variant={item.selected ? "outlined" : "text"}
          />
        )}
      />
    ) : null;
  return { page, display, nb_pages: nb_pages(), setPage };
}
