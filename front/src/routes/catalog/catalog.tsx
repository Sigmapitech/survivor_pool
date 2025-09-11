import { useEffect, useState } from "react";
import "./catalog.scss";
import { API_BASE_URL } from "@/api_url";

interface Project {
  logo: string;
  name: string;
  description: string;
  worth: number;
  nugget: number;
  id: number;
}

export default function CatalogPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [filtered, setFiltered] = useState<Project[]>([]);
  const [filter, setFilter] = useState({
    name: "",
    description: "",
    worth: "",
  });

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/projects/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data: Project[]) => {
        setProjects(data);
        setFiltered(data);
      });
  }, []);

  useEffect(() => {
    setFiltered(
      projects.filter((p) => {
        const nameMatch = p.name
          .toLowerCase()
          .includes(filter.name.toLowerCase());
        const descMatch = p.description
          .toLowerCase()
          .includes(filter.description.toLowerCase());
        const worthMatch =
          filter.worth === "" ||
          p.worth === Number(filter.worth) ||
          p.worth.toString().includes(filter.worth.replace(/\D/g, "")); // partial match
        return nameMatch && descMatch && worthMatch;
      })
    );
  }, [filter, projects]);

  return (
    <div className="catalog">
      <h1>Project Catalog</h1>
      <form className="catalog-filter">
        <input
          type="text"
          placeholder="Filter by name"
          value={filter.name}
          onChange={(e) => setFilter((f) => ({ ...f, name: e.target.value }))}
        />
        <input
          type="text"
          placeholder="Filter by description"
          value={filter.description}
          onChange={(e) =>
            setFilter((f) => ({ ...f, description: e.target.value }))
          }
        />
        <input
          type="number"
          placeholder="Filter by worth"
          value={filter.worth}
          onChange={(e) => setFilter((f) => ({ ...f, worth: e.target.value }))}
        />
      </form>
      <div className="catalog-list">
        {filtered.length === 0 ? (
          <p className="empty">No projects found.</p>
        ) : (
          filtered.map((project, _idx) => (
            <div className="gradient-card catalog-card" key={project.id}>
              <div className="catalog-card-image">
                <img
                  src={
                    project.logo.startsWith("app/static")
                      ? `${API_BASE_URL}/${project.logo.substring(4)}`
                      : project.logo
                  }
                  alt={project.name}
                  onError={(e) => {
                    (e.currentTarget as HTMLImageElement).src =
                      "https://placehold.co/200x200/EED5FB/31343C";
                  }}
                />
              </div>
              <div className="catalog-card-meta">
                <h2>{project.name}</h2>
                <p>{project.description}</p>
                <div className="catalog-card-info">
                  <span className="worth">Worth: {project.worth}</span>
                  <span className="nugget">Likes: {project.nugget}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
