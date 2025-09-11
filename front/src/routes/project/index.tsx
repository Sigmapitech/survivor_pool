import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { API_BASE_URL } from "@/api_url";

export interface Project {
  id: number;
  logo: string;
  name: string;
  description: string;
  worth: number;
  nugget: number;
  startup_id: number;
}

interface Founder {
  name: string;
  id: number;
  startup_id: number;
}

export interface Startup {
  id: number;
  name: string;
  legal_status: string;
  address: string;
  email: string;
  phone: string;
  sector: string;
  maturity: string;
  created_at: Date;
  description: string;
  website_url: string;
  social_media_url: string;
  project_status: string;
  needs: string;
  founders: Founder[];
  news: string;
}

export default function ProjectPage() {
  const { id } = useParams<{ id: string }>();
  const [project, setProjects] = useState<Project>();
  const [startup, setStartup] = useState<Startup>();

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/projects/${id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((project: Project) => setProjects(project))
      .catch(console.error);
  }, [id]);

  useEffect(() => {
    if (project?.startup_id === undefined) return;
    fetch(`${API_BASE_URL}/api/startups/${project?.startup_id}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((res) => res.json())
      .then((startup: Startup) => setStartup(startup))
      .catch(console.error);
  }, [project?.startup_id]);

  if (!project) return <p>"Loading project..."</p>;
  return (
    <div>
      <div className="project-id" key={project.id}>
        <h3>{project.name}</h3>
        <br />
        <img
          src={`${API_BASE_URL}/${project.logo}`}
          alt={project.name}
          className="project-logo"
          onError={(e) => {
            (e.currentTarget as HTMLImageElement).src =
              "https://placehold.co/600x400/EED5FB/31343C";
          }}
        />
        <div className="project-meta">
          <span>Founders:</span>
          {startup?.founders?.map((founder) => (
            <div key={founder.name} className="founder-name">
              {founder.name}
            </div>
          ))}
          <br />
          <span>Nuggets: {project.nugget}</span>
          <br />
          <span>{project.description}</span>
          <br />
          <span>Progress: {startup?.project_status}</span>
          <br />
          <span>Needs: {startup?.needs}</span>
          <div className="social-media">
            <span>Contact</span>
            <ul>Email: {startup?.email}</ul>
            <ul>Phone number: {startup?.phone}</ul>
            <ul>Site: {startup?.website_url}</ul>
            <ul>Other media: {startup?.social_media_url}</ul>
          </div>
        </div>
      </div>
    </div>
  );
}
