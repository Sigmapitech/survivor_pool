import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";
import "./home.scss";

export interface Project {
  id: number;
  logo: string;
  name: string;
  description: string;
  worth: number;
  nugget: number;
  startup_id: number;
}

function Project({ project }: { project: Project }) {
  return (
    <div className="project-card" key={project.id}>
      <img
        src={`${API_BASE_URL}/${project.logo}`}
        alt={project.name}
        className="project-logo"
        onError={(e) => {
          (e.currentTarget as HTMLImageElement).src =
            "https://placehold.co/600x400/EEE/31343C";
        }}
      />
      <h3>{project.name}</h3>
      <p>{project.description}</p>
      <div className="project-meta">
        <span>Worth: ${project.worth}</span>
        <span>Nuggets: {project.nugget}</span>
      </div>
    </div>
  );
}

export default function HomePage() {
  const [projects, setProjects] = useState<Project[] | null>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/projects/`)
      .then((res) => res.json())
      .then((list: Project[]) => setProjects(list))
      .catch(console.error);
  }, []);

  return (
    <>
      <section className="hero">
        <p>
          Uniting breakthrough ideas with global capital. We fast-track
          early-stage startups by providing funding, expertise, and an
          unparalleled international network.
        </p>
      </section>

      <section className="projects">
        <h2>Projects</h2>
        <div className="project-list">
          {projects === null ? (
            <p>Loading projects...</p>
          ) : projects.length === 0 ? (
            <p>No projects available at the moment.</p>
          ) : (
            projects.map((project) => (
              <Project key={project.id} project={project} />
            ))
          )}
        </div>
      </section>
    </>
  );
}
