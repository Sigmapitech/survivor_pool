import { type ChangeEvent, useState } from "react";
import { Link, useNavigate } from "react-router";

import "../auth.scss";

import { API_BASE_URL } from "@/api_url.ts";
import FormField from "@/components/form/field";
import FormSubmitButton, {
  handleFormSubmit,
} from "@/components/form/submit-button";

export default function VerifyPage() {
  const navigate = useNavigate();

  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    code: "",
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    setError("");

    if (!e.currentTarget.checkValidity()) return;
    e.preventDefault();

    handleFormSubmit({
      url: `${API_BASE_URL}/api/auth/verify`,
      body: formData,
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
        <FormField
          type="text"
          name="code"
          label="verification code"
          placeholder="123456"
          value={formData.code}
          onChange={handleChange}
        />

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <FormSubmitButton value="Sign in" />
        </div>
      </form>
      <Link to="/auth/register">Create an account</Link>
    </div>
  );
}
