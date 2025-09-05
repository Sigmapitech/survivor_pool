import { Outlet } from "react-router";
import NavigationBar from "./navigation-bar";

import "./main.scss";

export default function MainLayout() {
  return (
    <>
      <header>
        <NavigationBar />
      </header>
      <main>
        <Outlet />
      </main>
      <footer></footer>
    </>
  );
}
