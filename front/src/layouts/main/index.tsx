import { Outlet } from "react-router";
import NavigationBar from "./navigation-bar";

import "./main.css";

export default function Main() {
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
