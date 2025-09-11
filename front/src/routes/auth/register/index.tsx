import type { ChangeEvent, FormEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

import { API_BASE_URL } from "@/api_url";

import "../auth.scss";

interface ValidationErrorItem {
  loc: (string | number)[];
  msg: string;
  type: string;
}

const REGISTRATION_FIELDS = [
  {
    label: "Email",
    name: "email",
    type: "email",
    placeholder: "Email",
    pattern: "^[\\w.-]+@[\\w.-]+\\.\\w{2,}$",
    title: "Please enter a valid email address",
  },
  {
    label: "Username",
    name: "username",
    type: "text",
    placeholder: "Username",
    pattern: "^[a-zA-Z0-9_]{3,20}$",
    title: "3-20 characters, letters, numbers, underscores only",
  },
  {
    label: "Invitation Code",
    name: "invitation",
    type: "text",
    placeholder: "777 777",
    pattern: "^\\d{3}\\s\\d{3}$",
    title: "Format: 777 777",
  },
  {
    label: "Password",
    name: "password",
    type: "password",
    placeholder: "Password",
    pattern: ".{6,}",
    title: "Minimum 6 characters",
  },
  {
    label: "Confirm your password",
    name: "confirmPassword",
    type: "password",
    placeholder: "Confirm your password",
    pattern: ".{6,}",
    title: "Must match the password",
  },
];

function RegisterForm() {
  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    email: "",
    username: "",
    invitation: "",
    password: "",
    confirmPassword: "",
  });

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
    <form onSubmit={handleSubmit}>
      {REGISTRATION_FIELDS.map((field) => (
        <div className="auth-box" key={field.name}>
          <label htmlFor={field.name}>{field.label}</label>
          <input
            type={field.type}
            name={field.name}
            placeholder={field.placeholder}
            value={formData[field.name as keyof typeof formData]}
            onChange={handleChange}
            required
            pattern={field.pattern}
            title={field.title}
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
  );
}

export default function RegisterPage() {
  return (
    <div className="auth">
      <div className="auth-header">
        <Link to="/">←</Link>
        <h1>Register</h1>
      </div>

      <RegisterForm />

      <Link to="/auth/login">Already have an account?</Link>
    </div>
  );
}
