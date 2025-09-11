import { format, getDay, parse, startOfWeek } from "date-fns";
import { enUS } from "date-fns/locale/en-US";
import { useEffect, useState } from "react";
import { Calendar, dateFnsLocalizer } from "react-big-calendar";
import "react-big-calendar/lib/css/react-big-calendar.css";
import "./calendar.scss";
import { API_BASE_URL } from "@/api_url";

const locales = {
  "en-US": enUS,
};
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

interface Event {
  id: number;
  name: string;
  dates: string;
  location: string;
  description: string;
  event_type: string;
  target_audience: string;
}

function parseDates(dates: string): { start: Date; end: Date } {
  const [startStr, endStr] = dates.split(" to ");
  const start = parse(startStr, "yyyy-MM-dd", new Date());
  const end = endStr ? parse(endStr, "yyyy-MM-dd", new Date()) : start;
  return { start, end };
}

interface CalendarEvent {
  id: number;
  title: string;
  start: Date;
  end: Date;
  allDay: boolean;
  resource: Event;
}

export default function CalendarPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [filtered, setFiltered] = useState<Event[]>([]);
  const [filter, setFilter] = useState({
    name: "",
    type: "",
    location: "",
  });

  const [calendarMode, setCalendarMode] = useState<boolean>(false);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/events`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
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

  const calendarEvents: CalendarEvent[] = filtered.map((event) => {
    const { start, end } = parseDates(event.dates);
    return {
      id: event.id,
      title: `${event.name} (${event.event_type || "Other"})`,
      start,
      end,
      allDay: true,
      resource: event,
    };
  });

  return (
    <div className="calendar">
      <h1>Upcoming Events</h1>

      {/* Filters */}
      <form className="calendar-filter">
        <div>
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
          {/* Toggle between list/calendar */}
          <label className="mode-toggle">
            <input
              type="checkbox"
              checked={calendarMode}
              onChange={(e) => setCalendarMode(e.target.checked)}
            />
            {calendarMode ? "Calendar View" : "List View"}
          </label>
        </div>
      </form>

      {/* Render list OR calendar */}
      {calendarMode ? (
        <div
          style={{
            background: "#23232a",
            borderRadius: "12px",
            padding: "1em",
          }}
        >
          <Calendar
            localizer={localizer}
            events={calendarEvents}
            startAccessor="start"
            endAccessor="end"
            style={{ height: 600, color: "#e4bef8", background: "#23232a" }}
            eventPropGetter={() => ({
              style: {
                backgroundColor: "#c174f2",
                color: "#18181a",
                borderRadius: "6px",
                border: "none",
              },
            })}
            tooltipAccessor={(event: CalendarEvent) =>
              `${event.resource.description}\nLocation: ${event.resource.location}\nAudience: ${event.resource.target_audience}`
            }
          />
        </div>
      ) : (
        <div className="calendar-list">
          {filtered.length === 0 ? (
            <p className="empty">No events found.</p>
          ) : (
            filtered.map((event) => (
              <div className="calendar-card gradient-card" key={event.id}>
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
      )}
    </div>
  );
}
