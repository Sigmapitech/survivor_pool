import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";

import Main from "./layouts/main";

import "./index.scss";

import StartupCRUDPage from "@/routes/admin/startup-crud";
import UserCRUDPage from "@/routes/admin/user-crud";
import Login from "@/routes/auth/login";
import Register from "@/routes/auth/register";
import CalendarPage from "@/routes/calendar/calendar";
import CatalogPage from "@/routes/catalog/catalog";
import Home from "@/routes/home";
import Image from "@/routes/image";
import NewsPage from "@/routes/news-feed";
import EnterprisePage from "./routes/enterprise/enterprise";
import ProjectPage from "./routes/project";

const root = document.getElementById("root");
if (!root) throw new Error("Root element not found");

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Routes>
      <Route element={<Main />}>
        <Route index element={<Home />} />
        <Route path="/news" element={<NewsPage />} />
        <Route path="/catalog" element={<CatalogPage />} />
        <Route path="/calendar" element={<CalendarPage />} />
      </Route>

      <Route path="/auth/login" element={<Login />} />
      <Route path="/auth/register" element={<Register />} />

      <Route path="/admin/startup-crud" element={<StartupCRUDPage />} />
      <Route path="/admin/user-crud" element={<UserCRUDPage />} />
      <Route path="/admin/startup/project-register" element={<Image />} />
      <Route path="/projectpage" element={<ProjectPage id={2} />} />
      <Route path="/enterprise" element={<EnterprisePage />} />
    </Routes>
  </BrowserRouter>
);
