import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";

export interface News {
  id: number;
  logo: string;
  location: string;
  title: string;
  category: string;
  startup_id: string;
  description: string;
  date: Date;
}

function Newss({ news }: { news: News }) {
  return (
    <div className="News" key={news.id}>
      <img
        src={`${API_BASE_URL}/${news.logo}`}
        alt={news.title}
        className="news-logo"
        onError={(e) => {
          (e.currentTarget as HTMLImageElement).src =
            "https://placehold.co/600x400/EED5FB/31343C";
        }}
      />
      <h3>{news.title}</h3>
      <p>{news.description}</p>
      <div className="news-meta">
        <span>Date: ${news.date.toString()}</span>
        <span>Placement: ${news.location}</span>
        <span>Category: {news.category}</span>
      </div>
    </div>
  );
}

export default function NewsPage() {
  const [news, setNews] = useState<News[] | null>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/news/`)
      .then((res) => res.json())
      .then((list: News[]) => setNews(list))
      .catch(console.error);
  }, []);

  return (
    <>
      <section className="news-feed">
        <h2>News</h2>
        <div className="news-list">
          {news === null ? (
            <p>Loading news...</p>
          ) : news.length === 0 ? (
            <p>No news available at the moment.</p>
          ) : (
            news.map((news) => <Newss key={news.id} news={news} />)
          )}
        </div>
      </section>
    </>
  );
}
