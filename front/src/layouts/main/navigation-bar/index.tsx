import { Link } from "react-router";

import "./navbar.scss";

export default function Navbar() {
  return (
    <div className="navbar">
      <Link to="/">Jeb incubator</Link>

      <div className="navbar-auth">
        <Link to="/auth/login">Login</Link>
        <Link to="/auth/register">Register</Link>
      </div>
    </div>
  );
}
