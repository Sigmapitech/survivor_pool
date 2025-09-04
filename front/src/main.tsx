import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";

import Home from "./routes";

import "./index.css";

const root = document.getElementById("root");
if (!root) throw new Error("Root element not found");

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Routes>
      <Route index element={<Home />} />
    </Routes>
  </BrowserRouter>
);
