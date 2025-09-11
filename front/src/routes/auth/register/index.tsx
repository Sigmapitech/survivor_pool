import type { ChangeEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

import { API_BASE_URL } from "@/api_url";

import "../auth.scss";

import FormField from "@/components/form/field";
import FormSubmitButton, {
  handleFormSubmit,
} from "@/components/form/submit-button";

const REGISTRATION_FIELDS = [
  {
    label: "Username",
    name: "username",
    type: "text",
    placeholder: "Username",
    pattern: "^[a-zA-Z0-9_]{3,20}$",
    title: "3-20 characters, letters, numbers, underscores only",
  },
  {
    label: "Email",
    name: "email",
    type: "email",
    placeholder: "Email",
    pattern: ".+@.+",
    title: "Please enter a valid email address",
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
    pattern: ".{8,}",
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

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    setError("");

    if (!e.currentTarget.checkValidity()) return;
    e.preventDefault();

    const { email, username, invitation, password, confirmPassword } = formData;

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const payload = {
      name: username,
      email,
      password,
      invitation_code: invitation,
    };

    handleFormSubmit({
      url: `${API_BASE_URL}/api/auth/register/`,
      body: payload,
      onSuccess: (data) => {
        localStorage.setItem("token", data.token);
        navigate("/auth/verify");
      },
      onError: (e) => {
        setError(e);
      },
    });
  };

  return (
    <form className="gradient-card" onSubmit={handleSubmit}>
      {REGISTRATION_FIELDS.map((field) => (
        <FormField
          key={field.name}
          value={formData[field.name as keyof typeof formData]}
          onChange={handleChange}
          {...field}
        />
      ))}

      {error && <p className="error">{error}</p>}

      <div className="actions">
        <FormSubmitButton value="Create your account now" />
      </div>
    </form>
  );
}

export default function RegisterPage() {
  return (
    <div className="auth">
      <div className="auth-header">
        <Link to="/">
          <span className="material-symbols-outlined">arrow_left_alt</span>
        </Link>
        <h1>Register</h1>
      </div>

      <RegisterForm />

      <Link to="/auth/login">Already have an account?</Link>
    </div>
  );
}
