import type { ChangeEvent, FormEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

import { API_BASE_URL } from "@/api_url";

interface ValidationErrorItem {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    invitation: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    const { email, username, invitation, password, confirmPassword } = formData;

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    try {
      const payload = {
        name: username,
        email,
        password,
        invitation_code: invitation,
      };

      const response = await fetch(`${API_BASE_URL}/api/auth/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const data = await response.json();
        if (data.detail && Array.isArray(data.detail)) {
          const messages = data.detail
            .map((d: ValidationErrorItem) => d.msg)
            .join(", ");
          throw new Error(messages);
        } else {
          throw new Error(data.message || "Registration failed");
        }
      }

      navigate("/auth/login");
    } catch (err) {
      if (err instanceof Error) setError(err.message);
      else setError("An unexpected error occurred");
    }
  };

  return (
    <div className="auth">
      <div className="auth-login-hint">
        <span>Already have an account?</span>
        <Link to="/auth/login">Sign in →</Link>
      </div>

      <h1>Create your account</h1>
      <p>
        Per platform policy, users are created on demand by our administrators.
        If you have been validated for account creation, please enter the code
        given by your email.
      </p>

      <form onSubmit={handleSubmit}>
        {[
          {
            label: "Email",
            name: "email",
            type: "email",
            placeholder: "Email",
          },
          {
            label: "Username",
            name: "username",
            type: "text",
            placeholder: "Username",
          },
          {
            label: "Invitation Code",
            name: "invitation",
            type: "text",
            placeholder: "777 777",
          },
          {
            label: "Password",
            name: "password",
            type: "password",
            placeholder: "Password",
          },
          {
            label: "Confirm your password",
            name: "confirmPassword",
            type: "password",
            placeholder: "Confirm your password",
          },
        ].map((field) => (
          <div className="auth-box" key={field.name}>
            <label htmlFor={field.name}>{field.label}</label>
            <input
              type={field.type}
              name={field.name}
              placeholder={field.placeholder}
              value={formData[field.name as keyof typeof formData]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <input
            className="btn btn-validate"
            type="submit"
            value="Create your account now"
          />
        </div>
      </form>
    </div>
  );
}
