import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";
import "./enterprise.scss";

interface Project {
  id: number;
  name: string;
  description: string;
  logo: string;
  worth: number;
  nugget: number;
  startup_id: number;
}

interface Startup {
  id: number;
  name: string;
  sector: string;
  email: string;
  maturity: string;
  description?: string;
}

export default function EnterprisePage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [startups, setStartups] = useState<Startup[]>([]);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [editingStartup, setEditingStartup] = useState<Startup | null>(null);

  // Project form states
  const [projectForm, setProjectForm] = useState({
    name: "",
    description: "",
    worth: "",
    startup_id: "",
  });
  const [logoType, setLogoType] = useState<"file" | "url">("file");
  const [logoFile, setLogoFile] = useState<File | null>(null);
  const [logoUrl, setLogoUrl] = useState("");

  // Startup form states
  const [startupForm, setStartupForm] = useState({
    name: "",
    sector: "",
    email: "",
    maturity: "",
    description: "",
  });

  // Fetch projects and startups
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/projects/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((res) => res.json())
      .then(setProjects);

    fetch(`${API_BASE_URL}/api/startups`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then(setStartups);
  }, []);

  async function handleProjectSubmit(e: React.FormEvent) {
    e.preventDefault();
    const method = editingProject ? "PUT" : "POST";
    const url = editingProject
      ? `${API_BASE_URL}/api/projects/${editingProject.id}`
      : `${API_BASE_URL}/api/projects/${projectForm.startup_id}`;

    const formData = new FormData();
    formData.append("name", projectForm.name);
    formData.append("description", projectForm.description);
    formData.append("worth", projectForm.worth);

    // Handle logo
    if (logoType === "file" && logoFile) {
      formData.append("logo", logoFile);
    } else if (logoType === "url" && logoUrl) {
      try {
        const res = await fetch(logoUrl);
        const blob = await res.blob();
        const file = new File([blob], "logo.jpg", { type: blob.type });
        formData.append("logo", file);
      } catch (err) {
        alert("Failed to fetch image from URL");
        return;
      }
    }

    fetch(url, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      method,
      body: formData,
    }).then(() => {
      resetProjectForm();
      refreshProjects();
    });
  }

  function handleEditProject(project: Project) {
    setEditingProject(project);
    setProjectForm({
      name: project.name,
      description: project.description,
      worth: project.worth.toString(),
      startup_id: project.startup_id.toString(),
    });
    if (project.logo) {
      setLogoType("url");
      setLogoUrl(project.logo);
      setLogoFile(null);
    } else {
      setLogoType("file");
      setLogoFile(null);
      setLogoUrl("");
    }
  }

  function handleDeleteProject(id: number) {
    fetch(`${API_BASE_URL}/api/projects/${id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      method: "DELETE",
    }).then(() => setProjects((prev) => prev.filter((p) => p.id !== id)));
  }

  function resetProjectForm() {
    setEditingProject(null);
    setProjectForm({
      name: "",
      description: "",
      worth: "",
      startup_id: "",
    });
    setLogoType("file");
    setLogoFile(null);
    setLogoUrl("");
  }

  function refreshProjects() {
    fetch(`${API_BASE_URL}/api/projects/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((res) => res.json())
      .then(setProjects);
  }

  // --- Startup CRUD ---
  function handleStartupSubmit(e: React.FormEvent) {
    e.preventDefault();
    const method = editingStartup ? "PUT" : "POST";
    const url = editingStartup
      ? `${API_BASE_URL}/api/startups/${editingStartup.id}`
      : `${API_BASE_URL}/api/startups/`;
    const body = JSON.stringify(startupForm);

    fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body,
    }).then(() => {
      resetStartupForm();
      refreshStartups();
    });
  }

  function handleEditStartup(startup: Startup) {
    setEditingStartup(startup);
    setStartupForm({
      name: startup.name,
      sector: startup.sector,
      email: startup.email,
      maturity: startup.maturity,
      description: startup.description || "",
    });
  }

  function handleDeleteStartup(id: number) {
    fetch(`${API_BASE_URL}/api/startups/${id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      method: "DELETE",
    })
      .then((res) => {
        if (res.status !== 204) return;
        setStartups((prev) => prev.filter((s) => s.id !== id));
      })
      .catch(console.error);
  }

  function resetStartupForm() {
    setEditingStartup(null);
    setStartupForm({
      name: "",
      sector: "",
      email: "",
      maturity: "",
      description: "",
    });
  }

  function refreshStartups() {
    fetch(`${API_BASE_URL}/api/startups`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((res) => res.json())
      .then(setStartups);
  }

  return (
    <div className="enterprise">
      <h1>Project & Startup Management</h1>

      {/* --- Projects Section --- */}
      <section>
        <h2>{editingProject ? "Edit Project" : "Add Project"}</h2>
        <form className="enterprise-form" onSubmit={handleProjectSubmit}>
          <input
            type="text"
            placeholder="Name"
            value={projectForm.name}
            onChange={(e) =>
              setProjectForm((f) => ({ ...f, name: e.target.value }))
            }
            required
          />
          <input
            type="text"
            placeholder="Description"
            value={projectForm.description}
            onChange={(e) =>
              setProjectForm((f) => ({ ...f, description: e.target.value }))
            }
            required
          />
          <input
            type="number"
            placeholder="Worth"
            value={projectForm.worth}
            onChange={(e) =>
              setProjectForm((f) => ({ ...f, worth: e.target.value }))
            }
          />
          <select
            value={projectForm.startup_id}
            onChange={(e) =>
              setProjectForm((f) => ({ ...f, startup_id: e.target.value }))
            }
            required
          >
            <option value="">Select Startup</option>
            {startups.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>

          {/* Logo selection */}
          <div className="logo-input-group">
            <div>
              <label>
                <input
                  type="radio"
                  name="logoType"
                  value="file"
                  checked={logoType === "file"}
                  onChange={() => setLogoType("file")}
                />{" "}
                Upload File
              </label>
              <label>
                <input
                  type="radio"
                  name="logoType"
                  value="url"
                  checked={logoType === "url"}
                  onChange={() => setLogoType("url")}
                />{" "}
                Use URL
              </label>
            </div>

            {logoType === "file" ? (
              <input
                type="file"
                accept="image/*"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    setLogoFile(e.target.files[0]);
                  }
                }}
              />
            ) : (
              <input
                type="text"
                placeholder="Logo URL"
                value={logoUrl}
                onChange={(e) => setLogoUrl(e.target.value)}
              />
            )}
          </div>

          <button type="submit">
            {editingProject ? "Update Project" : "Add Project"}
          </button>
          {editingProject && (
            <button type="button" onClick={resetProjectForm}>
              Cancel
            </button>
          )}
        </form>

        <div className="enterprise-list">
          {projects.map((project) => (
            <div className="enterprise-card" key={project.id}>
              <p>
                <strong>{project.name}</strong> ({project.description})
              </p>
              <div className="edit-actions">
                <button
                  onClick={() => handleEditProject(project)}
                  type="button"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteProject(project.id)}
                  type="button"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* --- Startups Section --- */}
      <section>
        <h2>{editingStartup ? "Edit Startup" : "Add Startup"}</h2>
        <form className="enterprise-form" onSubmit={handleStartupSubmit}>
          <input
            type="text"
            placeholder="Name"
            value={startupForm.name}
            onChange={(e) =>
              setStartupForm((f) => ({ ...f, name: e.target.value }))
            }
            required
          />
          <input
            type="text"
            placeholder="Sector"
            value={startupForm.sector}
            onChange={(e) =>
              setStartupForm((f) => ({ ...f, sector: e.target.value }))
            }
          />
          <input
            type="email"
            placeholder="Email"
            value={startupForm.email}
            onChange={(e) =>
              setStartupForm((f) => ({ ...f, email: e.target.value }))
            }
            required
          />
          <input
            type="text"
            placeholder="Maturity"
            value={startupForm.maturity}
            onChange={(e) =>
              setStartupForm((f) => ({ ...f, maturity: e.target.value }))
            }
          />
          <input
            type="text"
            placeholder="Description"
            value={startupForm.description}
            onChange={(e) =>
              setStartupForm((f) => ({ ...f, description: e.target.value }))
            }
          />
          <button type="submit">
            {editingStartup ? "Update Startup" : "Add Startup"}
          </button>
          {editingStartup && (
            <button type="button" onClick={resetStartupForm}>
              Cancel
            </button>
          )}
        </form>

        <div className="enterprise-list">
          {startups.map((startup) => (
            <div className="enterprise-card" key={startup.id}>
              <div>
                <strong>{startup.name}</strong> ({startup.sector})
              </div>
              <div className="edit-actions">
                <button
                  onClick={() => handleEditStartup(startup)}
                  type="button"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDeleteStartup(startup.id)}
                  type="button"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
