import CrudTable, { type CrudColumn } from "@/components/crud-editor";

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

const userColumns: CrudColumn<User>[] = [
  { field: "name", label: "Name" },
  { field: "email", label: "Email" },
  { field: "role", label: "Role" },
];

export default function UserCRUDPage() {
  return <CrudTable<User> entityPath="users" columns={userColumns} />;
}
