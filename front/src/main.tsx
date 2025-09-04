import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";

import Main from "./layouts/main";
import Home from "./routes/home";

import "./index.css";

const root = document.getElementById("root");
if (!root) throw new Error("Root element not found");

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Routes>
      <Route element={<Main />}>
        <Route index element={<Home />} />
      </Route>
    </Routes>
  </BrowserRouter>
);
