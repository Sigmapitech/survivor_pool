import type { FormEvent } from "react";

export { handleFormSubmit } from "./handleFormSubmit";

import "./style.scss";

interface FormSubmitButtonProps {
  value: string;
  className?: string;
  submitCallback: (e: FormEvent<HTMLFormElement>) => void;
}

export default function FormSubmitButton({
  value,
  className = "btn-validate",
  submitCallback,
}: FormSubmitButtonProps) {
  return (
    <button
      type="submit"
      className={className}
      onClick={(e) => {
        if (submitCallback) submitCallback(e);
      }}
    >
      {value}
    </button>
  );
}
