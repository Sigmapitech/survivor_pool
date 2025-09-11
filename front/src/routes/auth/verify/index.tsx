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

  const resendMail = async (e: any) => {
    e.preventDefault();

    try {
      await fetch(`${API_BASE_URL}/api/auth/resend`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
        },
      });
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="auth">
      <div className="auth-header">
        <Link to="/">
          <span className="material-symbols-outlined">arrow_left_alt</span>
        </Link>
        <h1>Verify</h1>
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

        <div className="multi-actions">
          <FormSubmitButton
            onClick={resendMail}
            className="btn-red"
            value="Resend mail"
          />
          <FormSubmitButton value="Validate" />
        </div>
      </form>
      <Link to="/auth/register">Create an account</Link>
    </div>
  );
}
