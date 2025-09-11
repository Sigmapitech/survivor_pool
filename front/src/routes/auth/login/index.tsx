import type { FormEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

import "../auth.scss";

import { API_BASE_URL } from "@/api_url.ts";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await response.json();

      localStorage.setItem("token", data.token);

      navigate("/dashboard");
    } catch (err) {
      setError(err?.message);
    }
  };

  return (
    <div className="auth">
      <div className="auth-header">
        <Link to="/">←</Link>
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
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <input className="btn btn-validate" type="submit" value="Sign in" />
        </div>
      </form>
      <Link to="/auth/register">Create an account</Link>
    </div>
  );
}
