import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router";

import "./navbar.scss";

export default function Navbar() {
  const [token, setToken] = useState<null | string>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    setToken(storedToken);
  }, []);

  const handleDisconnect = () => {
    localStorage.removeItem("token");
    setToken(null);
    navigate("/");
  };

  return (
    <div className="navbar">
      <Link className="navbar-title" to="/">
        JEB incubator
      </Link>

      <div className="navbar-right">
        <Link className="dash-in" to="/dashboard">
          Dashboard
        </Link>
        {!token && (
          <>
            <Link className="dash-in" to="/auth/login">
              Login
            </Link>
            <Link className="dash-in" to="/auth/register">
              Register
            </Link>
          </>
        )}
        {token && (
          // biome-ignore lint: keynote
          <a className="dash-in" onClick={handleDisconnect}>
            Disconnect
          </a>
        )}
      </div>
    </div>
  );
}
