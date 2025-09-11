import PasswordInput from "../password-input";

interface FormFieldProps {
  field: {
    name: string;
    label: string;
    type: string;
    placeholder?: string;
    pattern?: string;
    title?: string;
    autocomplete?: string;
  };
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function FormField({ field, value, onChange }: FormFieldProps) {
  return (
    <div className="auth-box">
      <label htmlFor={field.name}>{field.label}</label>

      {field.type === "password" ? (
        <PasswordInput
          name={field.name}
          value={value}
          onChange={onChange}
          placeholder={field.placeholder}
        />
      ) : (
        <input
          type={field.type}
          name={field.name}
          placeholder={field.placeholder}
          value={value}
          onChange={onChange}
          required
          pattern={field.pattern}
          title={field.title}
          autoComplete={field.autocomplete}
        />
      )}
    </div>
  );
}
