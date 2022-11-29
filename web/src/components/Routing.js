import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { URL_ROOT } from "constants";
import { ROUTES } from "routes";
import Layout from "components/Layout";

export default function Routing() {
  return (
    <Routes>
      <Route path={URL_ROOT} element={<Layout />}>
        {Object.values(ROUTES).map((props, i) => (
          <Route key={i} {...props} />
        ))}
      </Route>
      <Route path="*" element={<Navigate to={ROUTES.home.path} />} />
    </Routes>
  );
}
