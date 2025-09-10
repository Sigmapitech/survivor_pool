import { Link } from "react-router";

import "./navbar.scss";

export default function Navbar() {
  return (
    <div className="navbar">
      <Link className="navbar-title" to="/">
        JEB incubator
      </Link>

      <div className="navbar-right">
        <Link to="/auth/login">Projects</Link>
        <Link to="/auth/login">Login</Link>
        <Link to="/auth/register">Register</Link>
      </div>
    </div>
  );
}
