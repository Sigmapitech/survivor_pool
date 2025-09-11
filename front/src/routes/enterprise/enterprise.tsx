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
  const [projectForm, setProjectForm] = useState({
    name: "",
    description: "",
    logo: "",
    worth: "",
    startup_id: "",
  });
  const [startupForm, setStartupForm] = useState({
    name: "",
    sector: "",
    email: "",
    maturity: "",
    description: "",
  });

  // Fetch projects and startups
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/projects/`)
      .then((res) => res.json())
      .then(setProjects);

    fetch(`${API_BASE_URL}/api/startups`)
      .then((res) => res.json())
      .then(setStartups);
  }, []);

  // Project CRUD
  function handleProjectSubmit(e: React.FormEvent) {
    e.preventDefault();
    const method = editingProject ? "PUT" : "POST";
    const url = editingProject
      ? `${API_BASE_URL}/api/projects/${editingProject.id}`
      : `${API_BASE_URL}/api/projects/${projectForm.startup_id}`;
    const formData = new FormData();
    formData.append("name", projectForm.name);
    formData.append("description", projectForm.description);
    formData.append("worth", projectForm.worth);
    formData.append("logo", projectForm.logo);

    fetch(url, {
      method,
      body: formData,
    }).then(() => {
      setEditingProject(null);
      setProjectForm({
        name: "",
        description: "",
        logo: "",
        worth: "",
        startup_id: "",
      });
      // Refresh
      fetch(`${API_BASE_URL}/api/projects/`)
        .then((res) => res.json())
        .then(setProjects);
    });
  }

  function handleEditProject(project: Project) {
    setEditingProject(project);
    setProjectForm({
      name: project.name,
      description: project.description,
      logo: project.logo,
      worth: project.worth.toString(),
      startup_id: project.startup_id.toString(),
    });
  }

  function handleDeleteProject(id: number) {
    fetch(`${API_BASE_URL}/api/projects/${id}`, { method: "DELETE" }).then(() =>
      setProjects((prev) => prev.filter((p) => p.id !== id))
    );
  }

  // Startup CRUD
  function handleStartupSubmit(e: React.FormEvent) {
    e.preventDefault();
    const method = editingStartup ? "PUT" : "POST";
    const url = editingStartup
      ? `${API_BASE_URL}/api/startups/${editingStartup.id}`
      : `${API_BASE_URL}/api/startups`;
    const body = JSON.stringify(startupForm);

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body,
    }).then(() => {
      setEditingStartup(null);
      setStartupForm({
        name: "",
        sector: "",
        email: "",
        maturity: "",
        description: "",
      });
      // Refresh
      fetch(`${API_BASE_URL}/api/startups`)
        .then((res) => res.json())
        .then(setStartups);
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
    fetch(`${API_BASE_URL}/api/startups/${id}`, { method: "DELETE" }).then(() =>
      setStartups((prev) => prev.filter((s) => s.id !== id))
    );
  }

  return (
    <div className="enterprise">
      <h1>Project & Startup Management</h1>
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
            type="text"
            placeholder="Logo URL"
            value={projectForm.logo}
            onChange={(e) =>
              setProjectForm((f) => ({ ...f, logo: e.target.value }))
            }
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
          <button type="submit">
            {editingProject ? "Update Project" : "Add Project"}
          </button>
          {editingProject && (
            <button
              type="button"
              onClick={() => {
                setEditingProject(null);
                setProjectForm({
                  name: "",
                  description: "",
                  logo: "",
                  worth: "",
                  startup_id: "",
                });
              }}
            >
              Cancel
            </button>
          )}
        </form>
        <div className="enterprise-list">
          {projects.map((project) => (
            <div className="enterprise-card" key={project.id}>
              <div>
                <strong>{project.name}</strong> ({project.description})
              </div>
              <div>
                <button onClick={() => handleEditProject(project)}>Edit</button>
                <button onClick={() => handleDeleteProject(project.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
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
            <button
              type="button"
              onClick={() => {
                setEditingStartup(null);
                setStartupForm({
                  name: "",
                  sector: "",
                  email: "",
                  maturity: "",
                  description: "",
                });
              }}
            >
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
              <div>
                <button onClick={() => handleEditStartup(startup)}>Edit</button>
                <button onClick={() => handleDeleteStartup(startup.id)}>
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
