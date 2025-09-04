import { BrowserRouter, Routes, Route } from "react-router";
import ReactDOM from "react-dom/client";

import Home from "./routes";

import './index.css'

const root = document.getElementById("root")!;

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Routes>
      <Route index element={<Home />} />
    </Routes>
  </BrowserRouter>,
);
