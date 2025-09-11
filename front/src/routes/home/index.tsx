import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";
import "./home.scss";
import { Link } from "react-router";

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
      <div className="project-card-meta">
        <h3>{project.name}</h3>
        <p>{project.description}</p>
      </div>
      <div className="project-card-image">
        <img
          src={`${API_BASE_URL}/${project.logo}`}
          alt={project.name}
          onError={(e) => {
            (e.currentTarget as HTMLImageElement).src =
              "https://placehold.co/200x200/EED5FB/31343C";
          }}
        />
      </div>
    </div>
  );
}

export default function HomePage() {
  const [projects, setProjects] = useState<Project[] | null>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/projects/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((res) => res.json())
      .then((list: Project[]) => setProjects(list.slice(0, 5)))
      .catch(console.error);
  }, []);

  return (
    <>
      <section className="hero">
        <img height="160px" src="logo.png" alt="J.E.B." />
        <div className="hero-description">
          <p>
            Discover a <strong>dynamic hub</strong> designed to{" "}
            <strong>empower startups</strong> and showcase groundbreaking
            innovation. Our platform{" "}
            <strong>highlights visionary founders</strong>, ambitious projects,
            and disruptive solutions across multiple industries. From{" "}
            <strong>early-stage ideas to market-ready ventures</strong>, we
            provide visibility into the inspiring journey of entrepreneurs
            shaping the future.
          </p>
          <Link className="arrow-link" to="login">
            Enroll your startup & get funds
          </Link>
        </div>
      </section>

      <section className="project-list">
        {projects === null ? (
          <p>Loading projects...</p>
        ) : projects.length === 0 ? (
          <p>No projects available at the moment.</p>
        ) : (
          projects.map((project) => (
            <Project key={project.id} project={project} />
          ))
        )}
      </section>
    </>
  );
}
