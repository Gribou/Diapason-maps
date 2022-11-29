import { configureStore } from "@reduxjs/toolkit";
import { setupListeners } from "@reduxjs/toolkit/query";
import { logger } from "redux-logger";

import { DEBUG } from "constants";
import api from "features/api";

const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware, ...(DEBUG ? [logger] : [])),
});

setupListeners(store.dispatch);

export default { store };
