import { useState } from "react";
import { Link, useNavigate } from "react-router";

import "../auth.scss";

import { API_BASE_URL } from "@/api_url.ts";
import PasswordInput from "@/components/form/password-input";
import FormSubmitButton, {
  handleFormSubmit,
} from "@/components/form/submit-button";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    setError("");

    if (!e.currentTarget.checkValidity()) return;
    e.preventDefault();

    handleFormSubmit({
      url: `${API_BASE_URL}/api/auth/login`,
      body: { email, password },
      onSuccess: (data) => {
        localStorage.setItem("token", data.token);
        navigate("/dashboard");
      },
      onError: (err) => setError(err),
    });
  };

  return (
    <div className="auth">
      <div className="auth-header">
        <Link to="/">
          <span className="material-symbols-outlined">arrow_left_alt</span>
        </Link>
        <h1>Sign In to Jeb-Incubator</h1>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="auth-box">
          <label htmlFor="email">Email</label>
          <input
            type="text"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="auth-box">
          <label htmlFor="password">Password</label>
          <PasswordInput
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <FormSubmitButton value="Sign in" />
        </div>
      </form>
      <Link to="/auth/register">Create an account</Link>
    </div>
  );
}
