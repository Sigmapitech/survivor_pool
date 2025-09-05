import CrudTable, { type CrudColumn } from "@/components/crud-editor";

export interface Startup {
  id: number;
  name: string;
  sector: string;
  email: string;
  maturity: string;
}

const startupColumns: CrudColumn<Startup>[] = [
  { field: "name", label: "Name" },
  { field: "sector", label: "Sector" },
  { field: "email", label: "Email" },
  { field: "maturity", label: "Maturity" },
];

export default function StartupCRUDPage() {
  return <CrudTable<Startup> entityPath="startups" columns={startupColumns} />;
}
