import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";

import Main from "./layouts/main";
import Login from "./routes/auth/login";
import Register from "./routes/auth/register";
import Home from "./routes/home";

import "./index.scss";
import StartupCRUD from "@/routes/admin/startup-crud";

const root = document.getElementById("root");
if (!root) throw new Error("Root element not found");

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Routes>
      <Route element={<Main />}>
        <Route index element={<Home />} />
      </Route>
      <Route path="/auth/login" element={<Login />} />
      <Route path="/auth/register" element={<Register />} />
      <Route path="/admin/startup-crud" element={<StartupCRUD />} />
    </Routes>
  </BrowserRouter>
);
