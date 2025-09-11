export { handleFormSubmit } from "./handleFormSubmit";

import "./style.scss";

interface FormSubmitButtonProps {
  value: string;
  className?: string;
}

export default function FormSubmitButton({
  value,
  className = "btn-validate",
}: FormSubmitButtonProps) {
  return (
    <button type="submit" className={className}>
      {value}
    </button>
  );
}
