import { type ChangeEvent, useEffect, useState } from "react";

import "./crud-table.scss";

export interface CrudColumn<T> {
  field: keyof T;
  label: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
  editable?: boolean;
}

interface CrudTableProps<T> {
  apiBaseUrl: string;
  entityPath: string;
  columns: CrudColumn<T>[];
  idField?: keyof T;
}

const CrudTable = <T extends { id: number }>({
  apiBaseUrl,
  entityPath,
  columns,
  idField = "id" as keyof T,
}: CrudTableProps<T>) => {
  const [data, setData] = useState<T[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<Partial<T>>({});

  useEffect(() => {
    fetch(`${apiBaseUrl}/api/${entityPath}`)
      .then((res) => res.json())
      .then((list: T[]) => setData(list))
      .catch(console.error);
  }, [apiBaseUrl, entityPath]);

  const startEdit = (row: T) => {
    setEditingId(row[idField] as unknown as number);
    setFormData(row);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setFormData({});
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>, field: keyof T) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  const saveEdit = async () => {
    if (!editingId) return;
    const res = await fetch(`${apiBaseUrl}/api/${entityPath}/${editingId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (res.ok) {
      const updated: T = await res.json();

      updated[idField] = Number(updated[idField]); // TODO: fixup
      setData((prev) =>
        prev.map((row) => (row[idField] === updated[idField] ? updated : row))
      );
      cancelEdit();
    }
  };

  const deleteRow = async (id: number) => {
    if (!window.confirm("Delete this item?")) return;
    const res = await fetch(`${apiBaseUrl}/api/${entityPath}/${id}`, {
      method: "DELETE",
    });
    if (res.ok) {
      setData((prev) => prev.filter((row) => row[idField] !== id));
    }
  };

  return (
    <div className="crud-table">
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={String(col.field)}>{col.label}</th>
            ))}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row[idField] as unknown as string}>
              {columns.map((col) => (
                <td key={String(col.field)}>
                  {editingId === row[idField] && col.editable !== false ? (
                    <input
                      value={String(formData[col.field] ?? "")}
                      onChange={(e) => handleChange(e, col.field)}
                    />
                  ) : col.render ? (
                    col.render(row[col.field], row)
                  ) : (
                    String(row[col.field] ?? "")
                  )}
                </td>
              ))}
              <td>
                {editingId === row[idField] ? (
                  <div className="actions">
                    <button type="submit" className="save" onClick={saveEdit}>
                      Save
                    </button>
                    <button
                      type="submit"
                      className="cancel"
                      onClick={cancelEdit}
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <div className="actions">
                    <button type="submit" onClick={() => startEdit(row)}>
                      Edit
                    </button>
                    <button
                      type="submit"
                      className="delete"
                      onClick={() =>
                        deleteRow(row[idField] as unknown as number)
                      }
                    >
                      Delete
                    </button>
                  </div>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CrudTable;
