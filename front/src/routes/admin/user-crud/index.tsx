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

const UserCRUDPage = () => (
  <CrudTable<User>
    apiBaseUrl="http://localhost:8000"
    entityPath="users"
    columns={userColumns}
  />
);

export default UserCRUDPage;
