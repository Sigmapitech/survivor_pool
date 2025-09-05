import { type ChangeEvent, useEffect, useState } from "react";
import "./startup-crud.scss";
import { API_BASE_URL } from "@/api_url";

export interface Startup {
  id: number;
  name: string;
  sector: string;
  email: string;
  maturity: string;
}

const StartupCRUD = () => {
  const [startups, setStartups] = useState<Startup[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<Partial<Startup>>({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/startups`)
      .then((res) => res.json())
      .then((data: Startup[]) => setStartups(data))
      .catch(console.error);
  }, []);

  const startEdit = (startup: Startup) => {
    setEditingId(startup.id);
    setFormData(startup);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setFormData({});
  };

  const handleChange = (
    e: ChangeEvent<HTMLInputElement>,
    field: keyof Startup
  ) => {
    setFormData({ ...formData, [field]: e.target.value });
  };

  const saveEdit = async () => {
    if (!editingId) return;
    const res = await fetch(`${API_BASE_URL}/api/startups/${editingId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      const updated: Startup = await res.json();
      updated.id = Number(updated.id);

      setStartups((prev) =>
        prev.map((s) => (s.id === updated.id ? updated : s))
      );

      cancelEdit();
    }
  };

  const deleteStartup = async (id: number) => {
    if (!window.confirm("Delete this startup?")) return;
    const res = await fetch(`${API_BASE_URL}/api/startups/${id}`, {
      method: "DELETE",
    });
    if (res.ok) {
      setStartups((prev) => prev.filter((s) => s.id !== id));
    }
  };

  return (
    <div className="startup-table">
      <h2>Startup Editor</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Sector</th>
            <th>Email</th>
            <th>Maturity</th>
            <th className="actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          {startups.map((startup) => (
            <tr key={startup.id}>
              <td>
                {editingId === startup.id ? (
                  <input
                    value={formData.name || ""}
                    onChange={(e) => handleChange(e, "name")}
                  />
                ) : (
                  startup.name
                )}
              </td>
              <td>
                {editingId === startup.id ? (
                  <input
                    value={formData.sector || ""}
                    onChange={(e) => handleChange(e, "sector")}
                  />
                ) : (
                  startup.sector
                )}
              </td>
              <td>
                {editingId === startup.id ? (
                  <input
                    value={formData.email || ""}
                    onChange={(e) => handleChange(e, "email")}
                  />
                ) : (
                  startup.email
                )}
              </td>
              <td>
                {editingId === startup.id ? (
                  <input
                    value={formData.maturity || ""}
                    onChange={(e) => handleChange(e, "maturity")}
                  />
                ) : (
                  startup.maturity
                )}
              </td>
              <td className="actions">
                {editingId === startup.id ? (
                  <>
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
                  </>
                ) : (
                  <>
                    <button type="submit" onClick={() => startEdit(startup)}>
                      Edit
                    </button>
                    <button
                      type="submit"
                      className="delete"
                      onClick={() => deleteStartup(startup.id)}
                    >
                      Delete
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StartupCRUD;
