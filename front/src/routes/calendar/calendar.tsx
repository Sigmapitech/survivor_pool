import { useEffect, useState } from "react";
import "./calendar.scss";
import { API_BASE_URL } from "@/api_url";

interface Event {
  id: number;
  name: string;
  dates: string;
  location: string;
  description: string;
  event_type: string;
  target_audience: string;
}

export default function CalendarPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [filtered, setFiltered] = useState<Event[]>([]);
  const [filter, setFilter] = useState({
    name: "",
    type: "",
    location: "",
  });

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/events`)
      .then((res) => res.json())
      .then((data: Event[]) => {
        setEvents(data);
        setFiltered(data);
      });
  }, []);

  useEffect(() => {
    setFiltered(
      events.filter((e) => {
        const nameMatch = e.name
          .toLowerCase()
          .includes(filter.name.toLowerCase());
        const typeMatch = e.event_type
          ?.toLowerCase()
          .includes(filter.type.toLowerCase());
        const locationMatch = e.location
          ?.toLowerCase()
          .includes(filter.location.toLowerCase());
        return nameMatch && typeMatch && locationMatch;
      })
    );
  }, [filter, events]);

  return (
    <div className="calendar">
      <h1>Upcoming Events</h1>
      <form className="calendar-filter">
        <input
          type="text"
          placeholder="Filter by name"
          value={filter.name}
          onChange={(e) => setFilter((f) => ({ ...f, name: e.target.value }))}
        />
        <input
          type="text"
          placeholder="Filter by type"
          value={filter.type}
          onChange={(e) => setFilter((f) => ({ ...f, type: e.target.value }))}
        />
        <input
          type="text"
          placeholder="Filter by location"
          value={filter.location}
          onChange={(e) =>
            setFilter((f) => ({ ...f, location: e.target.value }))
          }
        />
      </form>
      <div className="calendar-list">
        {filtered.length === 0 ? (
          <p className="empty">No events found.</p>
        ) : (
          filtered.map((event) => (
            <div className="calendar-card" key={event.id}>
              <div className="calendar-card-meta">
                <h2>{event.name}</h2>
                <span className="type">{event.event_type || "Other"}</span>
                <span className="dates">{event.dates}</span>
                <span className="location">{event.location}</span>
                <p>{event.description}</p>
                <span className="audience">
                  Audience: {event.target_audience}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
