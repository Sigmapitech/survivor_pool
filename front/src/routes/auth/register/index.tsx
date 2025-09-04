import { Link } from "react-router";

export default function Login() {
  return (
    <div className="auth">
      <div className="auth-login-hint">
        <span>Already have an account?</span>
        <Link to="/auth/login">Sign in →</Link>
      </div>

      <h1>Create your account</h1>

      <form method="post" action="{{ url_for('auth.register_page') }}">
        <div className="auth-box">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            name="username"
            placeholder="Username"
            pattern="^([\w\d-]){4,32}$"
          />
        </div>
        <div className="auth-box">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            name="password"
            placeholder="Password"
            pattern="^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-_ @#$%^&+=]).*$"
          />
        </div>
        <div className="auth-box">
          <label htmlFor="confirm_password">Confirm your password</label>
          <input
            type="password"
            name="confirm_password"
            placeholder="confirm your password"
            pattern="^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-_ @#$%^&+=]).*$"
          />
        </div>
        <div className="actions">
          <input className="btn btn-validate" type="submit" value="Créer" />
        </div>
      </form>
    </div>
  );
}
