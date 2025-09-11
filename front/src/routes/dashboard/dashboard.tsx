import { Link } from "react-router";
import "./dashboard.scss";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";
import type { User } from "../admin/user-crud";

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data: User) => {
        setUser(data);
      })
      .catch(console.error);
  }, []);

  return (
    <div className="dashboard">
      <h1>Admin Dashboard</h1>
      <div className="dashboard-links dashboard-grid-3x2">
        {user?.role === "ADMIN" ? (
          <>
            <Link className="dashboard-card" to="/admin/user-crud">
              <span className="material-symbols-outlined">person</span>
              <div>
                <h2>User Management</h2>
                <p>Add, edit, delete users</p>
              </div>
            </Link>
            <Link className="dashboard-card" to="/admin/startup-crud">
              <span className="material-symbols-outlined">business</span>
              <div>
                <h2>Startup Management</h2>
                <p>Add, edit, delete startups</p>
              </div>
            </Link>
            <Link className="dashboard-card" to="/enterprise">
              <span className="material-symbols-outlined">folder</span>
              <div>
                <h2>Project/Startup Management</h2>
                <p>Manage projects and startup details</p>
              </div>
            </Link>
          </>
        ) : (
          <></>
        )}

        <Link className="dashboard-card" to="/catalog">
          <span className="material-symbols-outlined">view_list</span>
          <div>
            <h2>Project Catalog</h2>
            <p>View and filter all projects</p>
          </div>
        </Link>
        <Link className="dashboard-card" to="/calendar">
          <span className="material-symbols-outlined">calendar_month</span>
          <div>
            <h2>Events Calendar</h2>
            <p>View and filter events</p>
          </div>
        </Link>
        <Link className="dashboard-card" to="/news">
          <span className="material-symbols-outlined">newspaper</span>
          <div>
            <h2>News Feed</h2>
            <p>Latest news and updates</p>
          </div>
        </Link>
      </div>
    </div>
  );
}
