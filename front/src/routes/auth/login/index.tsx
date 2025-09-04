import { Link } from "react-router";
import "./auth.scss";

export default function Login() {
  return (
    <div className="auth">
      <div className="auth-header">
        <h1>Sign In to Jeb-Incubator</h1>
      </div>

      <form method="post">
        <div className="auth-box">
          <label htmlFor="username">Username</label>
          <input type="text" name="username" placeholder="" />
        </div>
        <div className="auth-box">
          <label htmlFor="password">Password</label>
          <input type="password" name="password" placeholder="" />
        </div>
        <div className="actions">
          <input className="btn btn-validate" type="submit" value="Sign in" />
        </div>
      </form>
      <Link to="/auth/register">Create an account</Link>
    </div>
  );
}
