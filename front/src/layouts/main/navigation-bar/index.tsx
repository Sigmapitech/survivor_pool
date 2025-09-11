import { Link } from "react-router";

import "./navbar.scss";

export default function Navbar() {
  return (
    <div className="navbar">
      <Link className="navbar-title" to="/">
        JEB incubator
      </Link>

      <div className="navbar-right">
        <Link className="dash-in" to="/catalog">
          Projects
        </Link>
        <Link className="dash-in" to="/dashboard">
          Dashboard
        </Link>
        <Link className="dash-in" to="/auth/login">
          Login
        </Link>
        <Link className="dash-in" to="/auth/register">
          Register
        </Link>
      </div>
    </div>
  );
}
