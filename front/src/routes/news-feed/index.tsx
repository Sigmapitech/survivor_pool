import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";

import "./style.scss";

export interface News {
  id: number;
  logo: string;
  location: string;
  title: string;
  category: string;
  startup_id: string;
  news_date: Date;
}

function News({ news }: { news: News }) {
  return (
    <div className="news gradient-card" key={news.id}>
      <p>{news.title}</p>
      <div className="news-meta">
        <span>{news.news_date.toString()}</span>
        <span>{news.location}</span>
      </div>
      <img
        src={`${API_BASE_URL}/api/news/${news.id}/image`}
        alt={news.title}
        className="news-logo"
        onError={(e) => {
          (e.currentTarget as HTMLImageElement).src =
            "https://placehold.co/600x400/EED5FB/31343C";
        }}
      />
    </div>
  );
}

export default function NewsPage() {
  const [news, setNews] = useState<News[] | null>(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/news/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    })
      .then((res) => res.json())
      .then((list: News[]) => setNews(list))
      .catch(console.error);
  }, []);

  if (news === null) {
    return (
      <section className="news-feed">
        <h1>News</h1>
        <div className="news-list">
          <p>Loading news...</p>
        </div>
      </section>
    );
  }

  if (news.length === 0) {
    return (
      <section className="news-feed">
        <div className="news-list">
          <p>No news available at the moment.</p>
        </div>
      </section>
    );
  }

  const grouped = news.reduce<Record<string, News[]>>((acc, item) => {
    const category = item.category || "Uncategorized";
    if (!acc[category]) acc[category] = [];
    acc[category].push(item);
    return acc;
  }, {});

  return (
    <section className="news-feed">
      <h1>News</h1>

      {Object.entries(grouped).map(([category, items]) => {
        const sortedItems = [...items].sort(
          (a, b) =>
            new Date(b.news_date).getTime() - new Date(a.news_date).getTime()
        );

        return (
          <section className="news-category" key={category}>
            <h3>{category}</h3>
            <div className="news-list">
              {sortedItems.map((n) => (
                <News key={n.id} news={n} />
              ))}
            </div>
          </section>
        );
      })}
    </section>
  );
}
